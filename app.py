from flask import Flask, render_template, request
import sqlite3
import datetime

app = Flask(__name__)

flag = 1

def get_conn():
    """Return a sqlite3 connection and ensure the `user` table exists."""
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            timestamp TEXT
        )
        """
    )
    conn.commit()
    c.close()
    return conn

@app.route("/",methods=["GET","POST"])
def index():
    global flag
    flag = 1
    return(render_template("index.html"))

@app.route("/main",methods=["GET","POST"])
def main():
    global flag

    if flag == 1:
        name = request.form.get("q")
        timestamp = datetime.datetime.now().isoformat()
        conn = get_conn()
        c = conn.cursor()
        c.execute("insert into user (name,timestamp) values(?,?)", (name, timestamp))
        conn.commit()
        c.close()
        conn.close()
        flag = 0
    return(render_template("main.html"))

@app.route("/paynow",methods=["GET","POST"])
def paynow():
    return(render_template("paynow.html"))

@app.route("/deposit",methods=["GET","POST"])
def deposit():
    return(render_template("deposit.html"))


@app.route("/userlog",methods=["GET","POST"])
def userlog():
    conn = get_conn()
    c = conn.cursor()
    c.execute("select * from user")
    rows = c.fetchall()
    r = "\n".join([str(row) for row in rows])
    c.close()
    conn.close()
    return(render_template("userlog.html", r=r))

@app.route("/deleteuserlog",methods=["GET","POST"])
def deleteuserlog():
    conn = get_conn()
    c = conn.cursor()
    c.execute("delete from user")
    conn.commit()
    c.close()
    conn.close()
    return(render_template("deleteuserlog.html"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
