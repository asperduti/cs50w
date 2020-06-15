import os
import requests
from flask import redirect, session, render_template
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def goodreads_lookup(isbn):
    """Look up book for isbn on Goodreads."""
    try:
        api_key = os.getenv("GOODREADS_API_KEY")
        response = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": api_key, "isbns": isbn})
        response.raise_for_status()
    except requests.RequestException:
        return None
    
    # Parse responde
    try:
        books = response.json()["books"]
        return {
            "isbn": books[0]["isbn"],
            "reviews_count": books[0]["reviews_count"],
            "average_rating": books[0]["average_rating"]
        }
    except (KeyError, TypeError, ValueError) as e:
        return None
