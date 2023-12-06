import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import INTEGER, VARCHAR, FLOAT
from sqlalchemy.orm import Mapped, mapped_column

# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()

# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) "
#                "NOT NULL, rating FLOAT NOT NULL)")
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J.k. Rowling', '9.3')")
# db.commit()

# create the extension
db = SQLAlchemy()

# create the app
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"

# initialize the app with the extension
db.init_app(app)


class Books(db.Model):
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR, unique=True, nullable=False)
    author: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    review: Mapped[float] = mapped_column(FLOAT, nullable=False)


with app.app_context():
    db.create_all()
    book = Books(title="Harry Potter", author="J. K. Rowling", review=9.3)
    db.session.add(book)
    db.session.commit()
