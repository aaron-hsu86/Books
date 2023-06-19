from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book_model, favorites_model

class User:

    DB = 'books_schema'
    tables = 'users'

    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []

    @classmethod
    def get_all(cls):
        query = f'SELECT * FROM {cls.tables};'
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        if results:
            for user in results:
                users.append( cls(user) )
        return users
    
    @classmethod
    def get_one(cls, id):
        query = f'SELECT * FROM {cls.tables} WHERE id = %(id)s;'
        data = {'id' : id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def save(cls, data):
        query = f'INSERT INTO {cls.tables} (name) VALUES (%(name)s);'
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = f'UPDATE {cls.tables} SET name = %(name)s WHERE id = %(id)s;'
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete(cls, id):
        query = f'DELETE FROM {cls.tables} WHERE id = %(id)s;'
        data = {'id' : id}
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_fav_books(cls, id):
        query =  '''SELECT * FROM users
                    LEFT JOIN favorites ON users.id = user_id
                    LEFT JOIN books ON books.id = book_id
                    WHERE users.id = %(id)s;'''
        data = {'id' : id}
        results = connectToMySQL(cls.DB).query_db( query, data )
        user = cls( results[0])
        if results:
            for row_from_db in results:
                book_data = {
                    'id' : row_from_db['books.id'],
                    'title' : row_from_db['title'],
                    'genre' : row_from_db['genre'],
                    'created_at' : row_from_db['books.created_at'],
                    'updated_at' : row_from_db['books.updated_at']
                }
                user.books.append(book_model.Book( book_data ) )
        return user.books
    
    @classmethod
    def not_fav_books(cls, id):
        query =  '''SELECT * FROM users
                    LEFT JOIN favorites ON users.id = user_id
                    JOIN books ON books.id = book_id
                    WHERE users.id != %(id)s;'''
        data = {'id' : id}
        results = connectToMySQL(cls.DB).query_db( query, data )
        user = cls( results[0])
        if results:
            for row_from_db in results:
                book_data = {
                    'id' : row_from_db['books.id'],
                    'title' : row_from_db['title'],
                    'genre' : row_from_db['genre'],
                    'created_at' : row_from_db['books.created_at'],
                    'updated_at' : row_from_db['books.updated_at']
                }
                user.books.append(book_model.Book( book_data ) )
        return user.books