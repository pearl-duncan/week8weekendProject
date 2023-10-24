from app import app, db
from flask import request, render_template, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user
from models import User, Book
from forms import LoginForm, SignUpForm, BookForm
from flask_login import login_user, logout_user


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

            new_user = User(first_name, last_name, username, password)
            db.session.add(new_user)
            db.session.commit()

            flash("You're signed up!", 'success')
            return redirect(url_for('index'))
        else:
             flash("Invalid form. Please try again", 'danger')
    return render_template('register.html')
            

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

            new_book = Book(title, summary, author)

            db.session.add(new_book)
            db.session.commit()

            flash("book saved!", 'success')
        else:
            flash("Invalid form. Please try again", 'danger')
    return render_template("index.html", form = form)

@app.route('/book/<book_id>')
@jwt_required
def ind_book(book_id):
    book = Book.query.filter_by(book_id)
    return render_template('ind_book.html', book=book)

@app.route('/reading_list', methods=['GET', 'POST'])
def readingList():
    books = Book.query.filter(User.user.id==current_user.id).all()
    return render_template('reading_list.html', books=books)

@app.route("/delete_book/<book_id")
@jwt_required
def delete(book_id):
    book = Book.query.filter(book_id).first_or_404()
    db.session.delete(book)
    db.session.commit()
    flash("that book has been removed from your list", 'danger')
    return redirect(url_for('reading_list'))

@app.route('/update_book/<book_id>')
@jwt_required
def update(book_id):
    form = BookForm()
    if request.method == "POST":
        if form.validate() and book_id==book_id:
            title = form.title.data
            summary = form.summary.data
            author = form.author.data

            updated_book = Book(title, summary, author)

            db.session.add(updated_book)
            db.session.commit()

            flash("Book has been updated!", 'success')
        else:
            flash("Invalid form, please try again", 'danger')
    return render_template('edit_book.html')


