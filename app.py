from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey123"


# =========================
# DATABASE
# =========================
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# INIT DATABASE
# =========================
def init_db():

    conn = get_db()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # BOOKINGS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            date TEXT,
            time TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


# =========================
# LOGIN
# =========================
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user"] = username

            return redirect("/dashboard")

        return "❌ Wrong username or password"

    return render_template("login.html")


# =========================
# REGISTER
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        password = generate_password_hash(
            request.form["password"]
        )

        conn = get_db()
        cursor = conn.cursor()

        try:

            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )

            conn.commit()

        except Exception as e:
            return f"❌ ERROR: {e}"

        conn.close()

        return redirect("/")

    return render_template("register.html")


# =========================
# DASHBOARD
# =========================
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    conn = get_db()
    cursor = conn.cursor()

    # USERS COUNT
    cursor.execute("SELECT COUNT(*) FROM users")
    users_count = cursor.fetchone()[0]

    # BOOKINGS COUNT
    cursor.execute("SELECT COUNT(*) FROM bookings")
    bookings_count = cursor.fetchone()[0]

    # LATEST BOOKINGS
    cursor.execute("""
        SELECT * FROM bookings
        ORDER BY id DESC
        LIMIT 5
    """)

    latest = cursor.fetchall()

    conn.close()

    return render_template(

    "dashboard.html",

    users=users_count,

    bookings=bookings_count,

    latest=latest,

    total_bookings=bookings_count,

    total_customers=bookings_count,

    revenue=bookings_count * 20
)

# =========================
# ADD BOOKING
# =========================
@app.route("/add-booking", methods=["POST"])
def add_booking():

    if "user" not in session:
        return redirect("/")

    name = request.form["name"]
    phone = request.form["phone"]
    date = request.form["date"]
    from datetime import datetime

    time_24 = request.form["time"]
    time = datetime.strptime(time_24, "%H:%M").strftime("%I:%M %p")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO bookings
        (name, phone, date, time, status)
        VALUES (?, ?, ?, ?, ?)
    """, (name, phone, date, time, "Pending"))

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# =========================
# DELETE BOOKING
# =========================
@app.route("/delete-booking/<int:id>")
def delete_booking(id):

    @app.route("/edit/<int:id>", methods=["GET", "POST"])
    def edit_booking(id):

     conn = sqlite3.connect("bookings.db")
     cursor = conn.cursor()

     if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        date = request.form["date"]
        time = request.form["time"]

        cursor.execute("""
        UPDATE bookings
        SET name=?, phone=?, date=?, time=?
        WHERE id=?
        """, (name, phone, date, time, id))

        conn.commit()
        conn.close()

        return redirect("/dashboard")
        cursor.execute("SELECT * FROM bookings WHERE id=?", (id,))
     booking = cursor.fetchone()

     conn.close()

     return render_template("edit.html", booking=booking)
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM bookings WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(hosts="0.0.0.0", port=10000)
    import pandas as pd
from flask import send_file
from sqlalchemy import text

@app.route('/export')
def export_excel():
    # هون بجيب كل الحجوزات من الداتا بيز
    with db.engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM booking"))  # بدلي booking باسم الجدول عندك
        bookings = [dict(row._mapping) for row in result]
    
    df = pd.DataFrame(bookings)
    file_path = "/tmp/bookings.xlsx"
    df.to_excel(file_path, index=False)
    
    return send_file(file_path, as_attachment=True, download_name="bookings.xlsx")