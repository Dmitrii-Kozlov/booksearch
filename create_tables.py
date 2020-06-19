import os
import csv
from flask import Flask

# Import table definitions.

from models import *

app = Flask(__name__)

# Tell Flask what SQLAlchemy databas to use.
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Link the Flask app with the database (no Flask app is actually being run yet).
db.init_app(app)


def main():
    # Create tables based on each table definition in `models`
    db.create_all()

    # Import books into table
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        book = Books(isbn=isbn, title=title, author=author,year=year)
        db.session.add(book)
    db.session.commit()

if __name__ == "__main__":
    # Allows for command line interaction with Flask application
    with app.app_context():
        main()
