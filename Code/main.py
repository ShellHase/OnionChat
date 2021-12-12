from flask import Flask, render_template, url_for, request, redirect
import sqlite3
from hashlib import sha512
import os
import re


app = Flask(__name__)


# defining User class for current user
class User:
    def __init__(self, name, password, img):
        self.name = name
        self.password = password
        self.img = img
        self.logged_in = False

# assigning new User to variable I which stands just for I
I = User('', '', '')


# --------------------------------------------/--------------------------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.referrer == "http://127.0.0.1:1234/login":
        # open connection
        admin_db = sqlite3.connect("static/db/admin.db")

        # checking if user is already registrated or not
        # if user registrated
        if len(admin_db.execute(f"SELECT * FROM user WHERE name = \"{request.form.get('name')}\"").fetchall()) > 0:
            if sha512(request.form.get("password").encode()).hexdigest() == \
                    admin_db.execute(f"SELECT password FROM user WHERE name = \"{request.form.get('name')}\"").fetchall()[0][0]:
                I.logged_in = True
            else:
                I.logged_in = False
                return redirect("/login")
        # if user not registrated
        else:
            admin_db.execute("INSERT INTO user (name, password, img) VALUES ('{}', '{}', '{}');".format(
            request.form.get("name"),
                sha512(request.form.get("password").encode()).hexdigest(),
                "badBoy.jpg"))
            I.logged_in = True


        # setting up user
        I.name = request.form.get("name")
        I.password = sha512(request.form.get("password").encode()).hexdigest()
        I.img = admin_db.execute(f"SELECT img FROM user WHERE name = \"{request.form.get('name')}\"").fetchall()[0][0]

        # commit changes and close connection
        admin_db.commit()
        admin_db.close()

    # rendering template with param log_in for login state
    return render_template("home.html", log_in=I.logged_in)


# --------------------------------------------/login--------------------------------------------
@app.route("/login")
def login():
    pwd_state = True
    if request.referrer == "http://127.0.0.1:1234/login":
        pwd_state = False
    # rendering template with param log_in for login state
    return render_template("login.html", log_in=I.logged_in, pwd_state=pwd_state)


# --------------------------------------------/discussion--------------------------------------------
@app.route("/discussion", methods=["GET", "POST"])
def discuss():
    # connecting for managing discussions
    db = sqlite3.connect("static/db/admin.db")
    # if method = post
    if request.method == "POST":
        cmd = request.form.get("cmd")
        # if command is + adding new discussion
        if cmd[0] == "+":
            count = 0
            for i in db.execute("SELECT name FROM discussions").fetchall():
                if i[0] == "newDiscussion" or re.search("newDiscussion_[0-9]", i[0]) is not None:
                    count += 1
            db.execute(f'INSERT INTO discussions VALUES '
                       f"(\"newDiscussion{'_' + str(count) if count != 0 else ''}\")")

        # removing discussion entry and .db file if exists
        if cmd[0] == "-":
            db.execute(f"DELETE FROM discussions WHERE name='{cmd[5:]}'")
            if os.path.exists(f"static/db/{cmd[5:]}.db"):
                os.remove(f"static/db/{cmd[5:]}.db")

        # renaming discussion
        if cmd == ".":
            db.execute(f"UPDATE discussions SET name='{''}'")


    discussions = db.execute("SELECT name FROM discussions").fetchall()
    db.commit()
    db.close()
    return render_template("discussList.html", discussions=discussions)


# --------------------------------------------/discussion/<name>--------------------------------------------
@app.route("/discussion/<name>", methods=["GET", "POST"])
def defaultDiscuss(name):
    # preparing user data for using
    pic = url_for('static', filename=f'images/{I.img}')

    # checking if discussion db and of course also the tables in it exist
    if not os.path.exists(f"./static/db/{name}.db"):
        # open connection for displaying and writing history and declaring tables
        discuss_conn = sqlite3.connect(f"./static/db/{name}.db")
        discuss_conn.execute("CREATE TABLE history (name, msg)")
        discuss_conn.execute("CREATE TABLE teilnehmer (name, img)")
        discuss_conn.commit()
    else:
        # open connection for displaying and writing history
        discuss_conn = sqlite3.connect(f"./static/db/{name}.db")

    if request.method == "POST":
        if request.referrer == f"http://127.0.0.1:1234/discussion/{name}":
            discuss_conn.execute("INSERT INTO history (name, msg) VALUES ('{}', '{}');".format(I.name, request.form.get('msg')))
            # if first time user writes, adding to teilnehmer
            if len(discuss_conn.execute("SELECT * FROM teilnehmer WHERE name = '{}'".format(I.name)).fetchall()) == 0:
                discuss_conn.execute(f"INSERT INTO teilnehmer (name, img) VALUES ('{I.name}', '{I.img}')")
            discuss_conn.commit()

    # preparing history
    history = []
    for name, msg in discuss_conn.execute("SELECT * FROM history").fetchall():
        history.append((name,
                        url_for('static', filename='images/' + discuss_conn.execute(f"SELECT img FROM teilnehmer WHERE name = '{name}'").fetchall()[0][0]),
                        msg))

    discuss_conn.close()

    # rendering template with params pro_pic for profile picture, history for chat history and log_ in for login state
    return render_template("discuss.html", pro_pic=pic, history=history, log_in=I.logged_in)


if __name__ == "__main__":
    app.run(port=1234)  # wenn debug mode alles wird noch einmal ausgeführt
