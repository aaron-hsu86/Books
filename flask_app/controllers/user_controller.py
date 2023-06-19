from flask_app import app
from flask import render_template, redirect, request
from flask_app.models import book_model, user_model, favorites_model

@app.route('/')
@app.route('/users')
def user_page():
    users = user_model.User.get_all()
    return render_template('users.html', users = users)

@app.route('/add_user', methods=['post'])
def add_user():
    user_model.User.save(request.form)
    return redirect('/users')

@app.route('/user/<int:id>')
def show_user(id):
    user = user_model.User.get_one(id)
    books = favorites_model.Faves.get_user_favBooks(id)
    not_fav_books = favorites_model.Faves.get_user_notFavBooks(id)
    return render_template('users_show.html',user=user, books = books, not_fav_books = not_fav_books)

@app.route('/add_book_to_user_fav', methods=['post'])
def add_book_to_user_fav():
    favorites_model.Faves.save(request.form)
    id = request.form['user_id']
    return redirect(f'/user/{id}')