import sqlite3

conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()

for table in ("players", "games", "users"):
    print(f"\n-- {table} --")
    cur.execute(f"SELECT * FROM {table}")
    cols = [d[0] for d in cur.description]
    print(cols)
    for row in cur.fetchall():
        print(row)

conn.close()
