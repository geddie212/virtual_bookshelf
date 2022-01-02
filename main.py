from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from secrets import token_hex
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Generate secret HEX key
app.config['SECRET_KEY'] = token_hex(16)
Bootstrap(app)
all_books = []


########## SQL WORK ##########
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    review = db.Column(db.Integer)


def add_book(title, author, rating):
    new_book = Books(title=title, author=author, review=rating)
    db.session.add(new_book)
    db.session.commit()


def show_books():
    every_book_sql = db.session.query(Books).all()
    all_books.clear()
    for book in every_book_sql:
        all_books.append({'id': book.id,
                          'title': book.title,
                          'author': book.author,
                          'rating': book.review})


def find_book(id):
    book_to_update = Books.query.get(id)
    return book_to_update


def edit_book_rating(id, review):
    book_to_update = Books.query.get(id)
    book_to_update.review = review
    db.session.commit()
    return book_to_update
##############################


class LibraryForm(FlaskForm):
    book_name = StringField('Book Name', validators=[DataRequired()])
    book_author = StringField('Author', validators=[DataRequired()])
    book_rating = SelectField('Rating', validators=[DataRequired()], choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    submit = SubmitField('Submit')

class EditReview(FlaskForm):
    book_rating = SelectField('Rating', validators=[DataRequired()], choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    submit = SubmitField('Amend')



@app.route('/', methods=['POST', 'GET'])
def home():
    show_books()
    return render_template('index.html', books=all_books)


@app.route('/add', methods=['POST', 'GET'])
def add():
    form = LibraryForm()
    if form.validate_on_submit():
        name = form.book_name.data
        author = form.book_author.data
        rating = form.book_rating.data
        add_book(name, author, rating)
        show_books()
        return render_template('index.html', books=all_books)
    else:
        return render_template('add.html', form=form)


@app.route('/edit_rating')
def edit_rating():
    return render_template('edit_rating.html')


@app.route('/edit_rating/<id>', methods=['POST', 'GET'])
def edit_rating_id(id):
    form = EditReview()
    chosen_book = find_book(id)
    if form.validate_on_submit():
        after_rating = form.book_rating.data
        print(after_rating)
        edit_book_rating(id, after_rating)
        show_books()
        return render_template('index.html', books=all_books)
    else:
        title = chosen_book.title
        author = chosen_book.author
        before_rating = chosen_book.review
        return render_template('edit_rating.html', form=form, title=title, author=author, rating=before_rating)


@app.route('/delete_book/<id>', methods=['POST', 'GET'])
def delete_book(id):
    book_to_delete = Books.query.get(id)
    db.session.delete(book_to_delete)
    db.session.commit()
    show_books()
    return render_template('index.html', books=all_books)


if __name__ == "__main__":
    app.run(debug=True)

