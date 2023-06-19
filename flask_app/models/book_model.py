from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model, favorites_model

class Book:

    DB = 'books_schema'
    tables = 'books'

    def __init__(self, data) -> None:
        self.id = data['id']
        self.title = data['title']
        self.genre = data['genre']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

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
        query = f'INSERT INTO {cls.tables} (title, genre) VALUES (%(title)s, %(genre)s);'
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = f'UPDATE {cls.tables} SET title = %(title)s, genre = %(genre)s WHERE id = %(id)s;'
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete(cls, id):
        query = f'DELETE FROM {cls.tables} WHERE id = %(id)s;'
        data = {'id' : id}
        return connectToMySQL(cls.DB).query_db(query, data)