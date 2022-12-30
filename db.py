import sqlite3
from database import sql_query

conn = sqlite3.connect("database/courses.db")

cursor = conn.cursor()

sql = sql_query.create_tables  # importamos las querys

cursor.execute(sql)
