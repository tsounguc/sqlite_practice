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
    # CRUD
    # CREATE A NEW RECORD
    book1 = Books(title="Harry Potter", author="J. K. Rowling", review=9.3)
    book2 = Books(title="The Black Panther", author="Charles Dickens", review=7.5)
    book3 = Books(title="Goku", author="Christian Tsoungui Nkoulou", review=7.5)
    db.session.add(book1)
    db.session.add(book2)
    db.session.add(book3)
    db.session.commit()

    # READ ALL RECORDS
    # create a "query" to select things from the database and order by title
    result = db.session.execute(db.select(Books).order_by(Books.title))
    all_books = result.scalars().all()
    for b in all_books:
        print(f"title: {b.title} author: {b.author} review: {b.review}")

    # READ A PARTICULAR RECORD BY QUERY
    book = db.session.execute(db.select(Books).where(Books.title == "Harry Potter")).scalar()
    print(book.title)

    # UPDATE A PARTICULAR RECORD BY QUERY
    book_to_update = db.session.execute(db.select(Books).where(Books.title == "The Black Panther")).scalar()
    book_to_update.title = "Black Panther"
    db.session.commit()

    # UPDATE A RECORD BY PRIMARY KEY
    book_id = 2
    book_to_update = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
    book_to_update.title = "Avatar The Last Air Bender"
    db.session.commit()

    # DELETE A PARTICULAR RECORD BY PRIMARY KEY
    book_id = 2
    book_to_delete = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()


