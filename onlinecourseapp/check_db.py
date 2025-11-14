import sqlite3

conn = sqlite3.connect("db.sqlite3")  # Connect to your database
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")  # Show all tables
tables = cursor.fetchall()

print("Tables in database:", tables)  # Output the table names

conn.close()
