import sqlite3
import time
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = "spendly-secret-key-change-in-production"

# Session timeout configuration (in seconds)
SESSION_IDLE_TIMEOUT = 1800  # 30 minutes
SESSION_ABSOLUTE_TIMEOUT = 86400  # 24 hours
SESSION_TIMEOUT_WARNING = 300  # 5 minutes before logout


def is_safe_redirect_url(target_url):
    """Validate that redirect URL is safe (same host, no open redirect)."""
    from urllib.parse import urlparse, urljoin

    if not target_url:
        return False

    parsed = urlparse(target_url)
    base_url = urljoin(request.host_url, "/")

    return target_url.startswith("/") or parsed.netloc == urlparse(request.host_url).netloc


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
        g.idle_deadline = None
    else:
        current_time = time.time()
        login_time = session.get("login_time")
        last_activity = session.get("last_activity")

        if login_time is None or last_activity is None:
            session.clear()
            return redirect(url_for("login"))

        time_since_login = current_time - login_time
        time_since_activity = current_time - last_activity

        if time_since_login > SESSION_ABSOLUTE_TIMEOUT:
            session.clear()
            return redirect(url_for("login", expired="true"))

        if time_since_activity > SESSION_IDLE_TIMEOUT:
            session.clear()
            return redirect(url_for("login", expired="true"))

        session["last_activity"] = current_time
        g.idle_deadline = current_time + (SESSION_IDLE_TIMEOUT - time_since_activity)

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
        g.user = cursor.fetchone()
        db.close()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if g.user is not None:
        return redirect(url_for("profile"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        error = None

        if not name:
            error = "Name is required."
        elif not email:
            error = "Email is required."
        elif not password:
            error = "Password is required."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        elif password != confirm_password:
            error = "Passwords do not match."

        if error is None:
            try:
                db = get_db()
                cursor = db.cursor()
                password_hash = generate_password_hash(password)
                cursor.execute(
                    "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                    (name, email, password_hash)
                )
                db.commit()
                user_id = cursor.lastrowid
                db.close()

                current_time = time.time()
                session["user_id"] = user_id
                session["login_time"] = current_time
                session["last_activity"] = current_time
                return redirect(url_for("profile"))
            except sqlite3.IntegrityError:
                error = "Email already registered."
                db.close()

        return render_template("register.html", error=error)

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if g.user is not None:
        return redirect(url_for("profile"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        error = None

        if not email:
            error = "Email is required."
        elif not password:
            error = "Password is required."

        if error is None:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT id, password_hash FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            db.close()

            if user is None:
                error = "Invalid email or password."
            elif not check_password_hash(user["password_hash"], password):
                error = "Invalid email or password."

        if error is None:
            current_time = time.time()
            session["user_id"] = user["id"]
            session["login_time"] = current_time
            session["last_activity"] = current_time

            next_page = request.args.get("next")
            if next_page and is_safe_redirect_url(next_page):
                return redirect(next_page)
            return redirect(url_for("profile"))

        return render_template("login.html", error=error)

    return render_template("login.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
@login_required
def profile():
    return f"Profile page — {g.user['name']}"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


def init_app():
    with app.app_context():
        init_db()
        seed_db()


if __name__ == "__main__":
    init_app()
    app.run(debug=True, port=5001)
