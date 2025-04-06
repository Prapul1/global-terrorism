import sqlite3

conn = sqlite3.connect('database.db')  # or your path
c = conn.cursor()

# Create the users table
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
''')

conn.commit()
conn.close()
print("✅ Database initialized")
