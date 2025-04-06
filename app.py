
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql
import os

app = Flask(_name_)
app.secret_key = 'pooja123'

# Initialize database if not exists
def init_db():
    if not os.path.exists("user.db"):
        conn = sql.connect("user.db")
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
                        sno INTEGER PRIMARY KEY AUTOINCREMENT,
                        RNAME TEXT NOT NULL,
                        ATTACK_TYPE TEXT NOT NULL,
                        CASES INTEGER NOT NULL)''')
        conn.commit()
        conn.close()

@app.route('/')
@app.route('/index')
def index():
    conn = sql.connect("user.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    conn.close()
    return render_template('index.html', datas=data)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/countries')
def countries():
    return render_template('countries.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/attack-motive')
def attack_motive():
    return render_template('attack_motive.html')

@app.route('/awareness')
def awareness():
    return render_template('awareness.html')

@app.route('/get')
def get():
    return render_template('get.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route("/add_user", methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        rname = request.form['rname']
        attack_type = request.form['attack_type']
        cases = request.form['cases']

        try:
            cases = int(cases)
        except ValueError:
            flash('Invalid case count. Must be a number.', 'danger')
            return redirect(url_for("add_user"))

        conn = sql.connect("user.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO users (RNAME, ATTACK_TYPE, CASES) VALUES (?, ?, ?)", (rname, attack_type, cases))
        conn.commit()
        conn.close()
        flash('Details added successfully!', 'success')
        return redirect(url_for("index"))

    return render_template("add_user.html")

@app.route("/edit_user/<int:sno>", methods=['POST', 'GET'])
def edit_user(sno):
    conn = sql.connect("user.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()

    if request.method == 'POST':
        rname = request.form['rname']
        attack_type = request.form['attack_type']
        cases = request.form['cases']

        try:
            cases = int(cases)
        except ValueError:
            flash('Invalid case count. Must be a number.', 'danger')
            return redirect(url_for("edit_user", sno=sno))

        cur.execute("UPDATE users SET RNAME=?, ATTACK_TYPE=?, CASES=? WHERE sno=?", (rname, attack_type, cases, sno))
        conn.commit()
        conn.close()
        flash('Details updated!', 'success')
        return redirect(url_for("index"))

    cur.execute("SELECT * FROM users WHERE sno=?", (sno,))
    data = cur.fetchone()
    conn.close()
    return render_template("edit_user.html", datas=data)

@app.route("/delete_user/<int:sno>", methods=['GET'])
def delete_user(sno):
    conn = sql.connect("user.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE sno=?", (sno,))
    conn.commit()
    conn.close()
    flash('Details deleted!', 'warning')
    return redirect(url_for("index"))

if _name_ == '_main_':
    init_db()  # Ensures DB and table is ready
    app.run(host='127.0.0.1', port=8005, debug=True)
