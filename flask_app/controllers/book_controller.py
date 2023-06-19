from flask_app import app
from flask import render_template, redirect, request
from flask_app.models import book_model, user_model, favorites_model

@app.route('/books')
def book_page():
    books = book_model.Book.get_all()
    return render_template('books.html', books = books)

@app.route('/add_book', methods=['post'])
def add_book():
    book_model.Book.save(request.form)
    return redirect('/books')

@app.route('/book/<int:id>')
def show_books(id):
    book = book_model.Book.get_one(id)
    users = favorites_model.Faves.get_book_favUsers(id)
    not_fav_users = favorites_model.Faves.get_book_notUserFav(id)
    return render_template('books_show.html', book = book, users = users, not_fav_users = not_fav_users)

@app.route('/add_user_to_book_fav', methods=['post'])
def add_user_to_book_fav():
    favorites_model.Faves.save(request.form)
    id = request.form['book_id']
    return redirect(f'/book/{id}')