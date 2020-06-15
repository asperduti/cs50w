import os

from flask import Flask, session, request, render_template, jsonify, redirect, url_for, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from helpers import login_required, apology, goodreads_lookup
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Make sure API key of Goodreads is set
if not os.environ.get("GOODREADS_API_KEY"):
    raise RuntimeError("GOODREADS_API_KEY not set")

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["DEBUG"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
@login_required
def index():
    return render_template("search.html")


@app.route("/search", methods=["GET","POST"])
@login_required
def search():
    """Look for in Isbn, Title and Author."""
    if request.method == "GET":
        return redirect(url_for("index"))
   
    term = request.form.get("value_searched", None)

    if term == None or term == "":
        flash("You must provide a term to search")
        return render_template("search.html")

    term = "%{}%".format(term)

    books = db.execute("SELECT * FROM books WHERE isbn LIKE :term OR title LIKE :term OR author LIKE :term;", {"term": term}).fetchall()
    
    if not len(books):
        flash("There is no books")

    return render_template("search.html", books=books)


@app.route("/book/<string:isbn>", methods=["GET"])
@login_required
def book(isbn):
    """Retrive indo of the given book."""
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn;", {"isbn": isbn}).fetchone()

    if book is None:
        return apology("ISBN not found on Database", code=404)

    reviews = db.execute("SELECT * FROM reviews JOIN users ON reviews.user_id=users.id WHERE book_id=:book_id ", {"book_id": book.id}).fetchall()

    current_user_review = db.execute("SELECT * FROM reviews WHERE book_id=:book_id AND user_id=:user_id", {"book_id": book.id, "user_id": session["user_id"]}).fetchone()

    book_extra = goodreads_lookup(isbn)

    if book_extra is not None:
        book = dict(book)
        book.update(book_extra)
    return render_template("book.html", book=book, reviews=reviews, current_user_review=current_user_review)


@app.route("/review/<string:isbn>", methods=["POST"])
@login_required
def review(isbn):
    """Save a user review."""
    review_text = request.form.get("review_text")
    review_rating = int(request.form.get("review_rating", 0))

    if review_text is None or review_text == "":
        flash("You must provide a review.")
    
    if review_rating is None or review_rating not in range(1, 6):
        flash("You must provide a rating between 1 to 5.")

    
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn;", {"isbn": isbn}).fetchone()

    if book is None:
        return apology("ISBN not found on Database", code=404)
    
    user_review = db.execute("SELECT * FROM reviews WHERE book_id=:book_id AND user_id=:user_id;", {"book_id": book.id, "user_id": session["user_id"]}).fetchone()

    if user_review is not None:
        return apology("You've alreadey submitted a review", code=403)
    
    db.execute("INSERT INTO reviews (user_id, book_id, score, review) VALUES (:user_id, :book_id, :score, :review);", {"user_id": session["user_id"], "book_id": book.id, "score": review_rating, "review": review_text})
    db.commit()
    return redirect(url_for("book", isbn=isbn))


@app.route("/api/<string:isbn>")
@login_required
def api_book(isbn):
    """Retrive info for the book."""
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn;", {"isbn": isbn}).fetchone()
    
    if book is None:
        return jsonify({"error": "ISBN not in database"}), 404

    book_extra = goodreads_lookup(isbn)

    if book_extra is not None:
        book = dict(book)
        book.update(book_extra)
    return jsonify(book)

@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.args.get("username")

    # Check that a username is provived
    if not username:
        return jsonify(False)

    # Look for users with that username
    users = db.execute("SELECT * FROM users WHERE username=:username", {"username":username}).fetchall()

    # Check if exist a user with that username
    if len(users):
        return jsonify(False)

    # The username is valid to use
    return jsonify(True)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure that username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure that username was submitted
        if not password:
            return apology("must provide password", 400)

        # Ensure that username was submitted
        if not confirmation:
            return apology("must provide confirmation password", 400)

        # Query database for username to check that not exist
        user = db.execute("SELECT * FROM users WHERE username = :username;",
                          {"username":username}).fetchall()

        # Check username available
        if user:
            return apology("username already taken", 400)

        # Check that password and confirmation are equal
        if confirmation != password:
            return apology("confirmation and password don't match", 400)

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :password);",
                   {"username":username, "password":generate_password_hash(password)})
        db.commit()
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          {"username":request.form.get("username")}).fetchall()
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")