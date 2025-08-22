#py code
from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# --- Vulnerable: Hardcoded secret key ---
app.secret_key = "mySuperSecretKey123"

# --- Vulnerable: No authentication on DB connection ---
def get_db_connection():
    conn = sqlite3.connect("users.db")
    return conn

@app.route("/search")
def search():
    # --- Vulnerable: SQL Injection ---
    username = request.args.get("username")
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"  # ❌ unsafe
    result = cursor.execute(query).fetchall()
    conn.close()
    return str(result)

@app.route("/rce")
def rce():
    # --- Vulnerable: Remote Code Execution ---
    cmd = request.args.get("cmd")
    output = os.popen(cmd).read()  # ❌ executes arbitrary commands
    return f"<pre>{output}</pre>"

@app.route("/xss")
def xss():
    # --- Vulnerable: Cross-Site Scripting (XSS) ---
    name = request.args.get("name", "Guest")
    return render_template_string(f"<h1>Welcome {name}</h1>")  # ❌ unsanitized

if __name__ == "__main__":
    app.run(debug=True)
