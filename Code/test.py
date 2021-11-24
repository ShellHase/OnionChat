import sqlite3

c = sqlite3.connect("./static/db/user.db")
print(c.execute("SELECT * FROM user").fetchall())
c.close()

c2 = sqlite3.connect("./static/db/nameDerDiskussion.db")
print(c2.execute("SELECT * FROM teilnehmer").fetchall())
print(c2.execute("SELECT * FROM history").fetchall())
c2.close()
