from app import app
from flask import request, render_template, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user
from .models import User, Book, db
from .forms import LoginForm, SignUpForm, BookForm
from flask_login import login_user, logout_user
from datetime import datetime



@app.route("/")
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
         return redirect(url_for('login'))
    form = SignUpForm()
    if request.method == "POST":
        if form.validate():
            first_name = form.first_name.data
            last_name = form.last_name.data
            username = form.username.data
            password = form.password.data

            user = User(first_name, last_name, username, password)
            db.session.add(user)
            db.session.commit()

            flash("You're signed up!", 'success')
            return redirect(url_for('index'))
        else:
             flash("Invalid form. Please try again", 'danger')
    return render_template('register.html', form=form)
            

@app.route('/login', methods =['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()

            if user:
                if user.password == password:
                    login_user(user)
                    flash("Successfully logged in", 'success')
                    return redirect(url_for('index'))
                else:
                    flash("Incorrect username/password combination, please try again", 'danger')
            else:
                flash("Thant username does not exist, please sign up first", 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@jwt_required
def logout():
    logout_user()
    flash("You have successfully logged out", 'success')
    return redirect(url_for('login_page'))

@app.route("/addBook")
@jwt_required
def add_book():
    form = BookForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            summary = form.summary.data
            author = form.author.data

            book = Book(title, summary, author)

            db.session.add(book)
            db.session.commit()

            flash("book saved!", 'success')
            return redirect(url_for('readingList'))
        else:
            flash("Invalid form. Please try again", 'danger')
    return render_template("add_book.html", form = form)

@app.route('/book/<book_id>')
@jwt_required
def ind_book(book_id):
    book = Book.query.get(book_id)
    return render_template('ind_book.html', b=book)

@app.route('/reading_list')
def readingList():
    book = Book.query.order_by(Book.date_created.desc()).all()
    return render_template('reading_list.html', b=book)

@app.route("/book/delete/<book_id", method=['GET', 'POST'])
@jwt_required
def delete(book_id):
    book = Book.query.filter(book_id).first_or_404()
    if not book:
        flash('that book does not exits', 'danger')
        return redirect(url_for('readingList'))
    if current_user.id != book.user_id:
        flash('You cannot delete someone else\'s book', 'danger')
        return redirect(url_for('ind_book', book_id=book_id))
    db.session.delete(book)
    db.session.commit()
    flash("that book has been removed from your list", 'danger')
    return redirect(url_for('readingList'))

@app.route('/update_book/<book_id>')
@jwt_required
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        flash("That book does not extist", 'danger')
        return redirect(url_for('readingList'))
    if current_user.id != book.user_id:
        flash('You cannot edit another persons book', 'danger')
        return redirect(url_for('ind_book', book_id=book_id))
    form = BookForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            summary = form.summary.data
            author = form.author.data

            book.title = title
            book.summary = summary
            book.author = author 
            book.last_updated = datetime.utcnow()

            db.session.commit()
            flash("Book has been updated!", 'success')
            return redirect(url_for('ind_book', book_id=book_id))
        
    return render_template('edit_book.html', b=book, form=form)


