# Project BookSearch with own database.



Project is a flask-application for searching books in own SQL database.

User can register with login and password, than login to website and search for books with following options:
- ISBN number
- title of the book
- author
- year of publication
On individual book page also showed rating from GoodReads.com and user can leave his review.
On /api/<isbn> is API available in JSON format with following answer:

{
  "author": "Stephen King", 
  "average_score": 0.0, 
  "isbn": "0451169514", 
  "review_count": 0, 
  "title": "It", 
  "year": 1986
}

Files in project:
books.csv - list of books
models.py - describing SQLAlchemy objects (tables)
create_table.py - create tables described in models.py
application.py - main flask application
HTML pages in "templates" folder:
-index.html - main screen with login/password welcome.
-register.html - registration page with login/password inputs (can be expanded by other fields).
-search.html - main search page with search fields(ISBN,title,author,year).
-result.html - page with results of search (title/author), each result is clickable.
-book.html - individual book page with added rating and reviews
-layout.html - layout page for project
-layout_login.html - layout page with logout button
-error.html - layout for any error
-success.html - layout for success action

