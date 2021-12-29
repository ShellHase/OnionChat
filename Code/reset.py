import sqlite3

c = sqlite3.connect("static/db/admin.db")
# c.execute("CREATE TABLE user(name, password, img)")
# c.execute("CREATE TABLE discussions(name)")
print(c.execute("SELECT * FROM user").fetchall())  # name password img
print(c.execute("SELECT * FROM discussions").fetchall())  # name
# c.execute("DELETE FROM user")
# c.execute("DELETE FROM discussions")
c.commit()
c.close()

c2 = sqlite3.connect("./static/db/defaultDiscussion.db")
# c2.execute("CREATE TABLE history (name, msg)")
# c2.execute("CREATE TABLE teilnehmer (name, img)")
print(c2.execute("SELECT * FROM history").fetchall())  # name msg
print(c2.execute("SELECT * FROM teilnehmer").fetchall())  # name img
# c2.execute("DELETE FROM history")
# c2.execute("DELETE FROM teilnehmer")
c2.commit()
c2.close()
