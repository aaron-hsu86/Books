# Miybe this should be added to other model files?

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book_model, user_model

class Faves:

    DB = 'books_schema'
    tables = 'favorites'

    def __init__(self, data) -> None:
        self.book_id = data['book_id']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = '''SELECT name, title, genre
                    FROM users
                    LEFT JOIN favorites ON users.id = user_id
                    LEFT JOIN books ON books.id = book_id;'''
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        if results:
            for user in results:
                users.append( cls(user) )
        return users
    
    @classmethod
    def get_user_favBooks(cls, id):
        query =  '''SELECT title, genre
                    FROM users
                    LEFT JOIN favorites ON users.id = user_id
                    LEFT JOIN books ON books.id = book_id
                    WHERE users.id = %(id)s;'''
        data = {'id' : id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def get_user_notFavBooks(cls, id):
        query =  '''
                SELECT books.id, title, genre FROM books
                LEFT JOIN favorites ON books.id = book_id
                LEFT JOIN users ON users.id = user_id
                EXCEPT
                SELECT book_id, title, genre FROM favorites
                LEFT JOIN books ON books.id = book_id
                LEFT JOIN users ON users.id = user_id
                WHERE users.id = %(id)s;'''
        data = {'id' : id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def save(cls, data):
        query = f'INSERT INTO {cls.tables} (book_id, user_id) VALUES ( %(book_id)s , %(user_id)s );'
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = f'''UPDATE {cls.tables}
                    SET book_id = %(books.id)s, user_id = %(users.id)s
                    WHERE id = %(id)s;'''
        return connectToMySQL(cls.DB).query_db(query, data)
    
    # @classmethod
    # def delete(cls, id):
    #     query = f'DELETE FROM {cls.tables} WHERE id = %(id)s;'
    #     data = {'id' : id}
    #     return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_book_favUsers(cls, id):
        query =  '''SELECT name
                    FROM books
                    LEFT JOIN favorites ON books.id = book_id
                    LEFT JOIN users ON users.id = user_id
                    WHERE books.id = %(id)s;'''
        data = {'id' : id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results

    @classmethod
    def get_book_notUserFav(cls, id):
        query = '''
                SELECT users.id, name FROM users
                LEFT JOIN favorites ON users.id = user_id
                LEFT JOIN books ON books.id = book_id
                EXCEPT
                SELECT user_id, name FROM favorites
                LEFT JOIN books ON books.id = book_id
                LEFT JOIN users ON users.id = user_id
                WHERE books.id = %(id)s;
                '''
        data = {'id' : id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results