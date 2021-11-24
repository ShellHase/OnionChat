from flask import Flask, render_template, url_for, request
import sqlite3

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    user = "SpongeBob"
    user_conn = sqlite3.connect("./static/db/user.db")  # um user zu teilnehmern hinzuzufügen (mit daten wie profilbild)
    img = user_conn.execute(f"SELECT img FROM user WHERE user = '{user}'").fetchall()[0][0]
    user_conn.close()

    pic = url_for('static', filename='sources/{}'.format(img))

    if request.method == "POST":
        discuss_conn = sqlite3.connect("./static/db/nameDerDiskussion.db")
        discuss_conn.execute("INSERT INTO history (user, msg) VALUES ('{}', '{}');".format(user, request.form.get('msg')))
        discuss_conn.commit()
        discuss_conn.close()

#    i = 0
#    while discuss_conn.execute(f"{i} IN user spalte index"):
#        blueprint = ""
#        i += 1

    return render_template("index.html", pro_pic=pic)


@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(port=1234)  # wenn debug mode alles wird noch einmal ausgeführt


"""
Dinge für später:

def new_user():
    c = sqlite3.connect("./static/db/user.db")
    c.execute("INSERT INTO user (user, img) VALUES ('{}', '{}');".format("SpongeBob", "SpongeBob.jpg"))
    c.commit()
    c.close()

def new_teilnehmer():
    discuss_conn = sqlite3.connect("./static/db/nameDerDiskussion.db")  # used for history und teilnehmer
    discuss_conn.execute("INSERT INTO teilnehmer (user, img) VALUES ('{}', '{}');".format("SpongeBob", "SpongeBob.jpg"))
    discuss_conn.commit()
    discuss_conn.close()
    
def new_userTable():
    c = sqlite3.connect("./static/db/user.db")
    c.execute("CREATE TABLE user (user TEXT, img TEXT);")
    c.commit()
    c.close()
    
def new_discussTable():
    discuss_conn = sqlite3.connect("./static/db/nameDerDiskussion.db")
    discuss_conn.execute("CREATE TABLE teilnehmer (user TEXT, img TEXT)")
    discuss_conn.execute("CREATE TABLE history (user Text, msg Text(350))")
    discuss_conn.commit()
    discuss_conn.close()
"""
