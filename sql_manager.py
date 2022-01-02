from flask import Flask, render_template, request, redirect, url_for
from secrets import token_hex
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Generate secret HEX key
app.config['SECRET_KEY'] = token_hex(16)
all_books = []

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Books(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    review = db.Column(db.Integer)


# db.create_all()
# book = Books(title='Tom', author='Tom', review=9)
# db.session.add(book)
# db.session.commit()

# book_to_update = Books.query.filter_by(title='Paul Ged').first()
# book_to_update.title = 'Ugne Ged'
# db.session.commit()
# print('Title Changed')

every_book = db.session.query(Books).all()
print(every_book[0].title)