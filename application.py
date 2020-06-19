import datetime
import os
import requests

from flask import Flask, render_template, request, session, jsonify
from flask_session import Session
from sqlalchemy import and_, func

from models import *

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    password = request.form.get("password")
    if name == '':
        return render_template("error.html", message="User should have a name.")
    user = Users(name=name, password=password)
    db.session.add(user)
    db.session.commit()
    return render_template("success.html", message="You have successfully registered!")

@app.route("/search", methods=["POST"])
def search():
    name = request.form.get("name")
    password = request.form.get("password")
    if name == '':
        return render_template("error.html", message="User should have a name.")

    user = Users.query.filter(and_(Users.name == name, Users.password == password)).first()

    if not user:
        return render_template("error.html", message="Invalid username or password.")
    print(user, user.name, user.password)
    session['id'] = user.id
    session['name'] = user.name
    year = datetime.date.today().year
    return render_template("search.html", year=year)

@app.route("/", methods=["POST"])
def logout():
    session['id'] = None
    session['name'] = None
    return render_template("index.html")
@app.route("/result", methods=["POST"])
def result():
    isbn = request.form.get("isbn")
    author = request.form.get("author").lower()
    title = request.form.get("title").lower()
    try:
        year = int(request.form.get("year"))
    except ValueError:
        return render_template("error.html", message="Year should be an integer.")
    year_pref = request.form.get("year_prefix")

    query = [Books.isbn.ilike(f'%{isbn}%'), Books.title.ilike(f'%{title}%'),
                                        Books.author.ilike(f'%{author}%')]
    if year_pref == '<':
        query.append(Books.year < year)
    elif year_pref == '>':
        query.append(Books.year > year)
    else:
        query.append(Books.year == year)

    books = Books.query.filter(and_(*query)).all()

    if not books:
        return render_template("error.html", message="No such book.")
    return render_template("result.html", books=books, book_count=len(books))

@app.route("/book/<int:book_id>")
def book(book_id):
    book = Books.query.get(book_id)
    if book is None:
        return render_template("error.html", message="No such book.")
    try:
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "XTPVONdDH1WsckYzB7SQ", "isbns": book.isbn})
        data = res.json()
        rating = data['books'][0]['average_rating']
        rating_count = data['books'][0]['work_ratings_count']
    except:
        rating = "unavailable"
        rating_count = "unavailable"
    # Get all reviews.
    reviews = Books.query.get(book_id).reviews
    return render_template("book.html", book=book, reviews=reviews, rating=rating, count=rating_count)

@app.route("/review/<int:book_id>", methods=["POST"])
def review(book_id):
    review = request.form.get("review")
    review_value = request.form.get("review_value")
    if not review:
        review = 'No comments.'
    temp = Reviews.query.filter(and_(Reviews.book_id == book_id, Reviews.user_id == session['id'])).count()
    if temp > 0:
        return render_template("error.html", message="You have already reviewed this book.")
    r = Reviews(review=review, book_id=book_id, user_id=session['id'], review_value=review_value)
    db.session.add(r)
    db.session.commit()
    return render_template("success.html", message="Your review successfully posted!")

@app.route("/api/<string:isbn>")
def isbn_api(isbn):

    book = Books.query.filter_by(isbn=isbn).first()
    if not book:
        return jsonify({'error':'No such book in database.'}), 404

    average_count= Reviews.query.with_entities(func.avg(Reviews.review_value)).filter_by(book_id=book.id).first()
    count = Reviews.query.filter_by(book_id=book.id).count()
    print(average_count, count)
    if average_count[0] is None:
        average_count = 0
    average_count = round(float(average_count[0]),2)
    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "review_count": count,
        "average_score": average_count
    })
