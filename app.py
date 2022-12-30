from flask import Flask, request, jsonify
from data import courses
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = None

    try:
        conn = sqlite3.connect("database/courses.db")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route('/courses', methods =['GET', 'POST'])
def home():

    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        
        cursor = conn.execute("SELECT * FROM courses")
        courses = cursor.fetchall()

        if courses:
            return jsonify({"courses":courses}), 200

        return jsonify({"messaje":"Nothign found"}), 404

    if request.method == 'POST':
        name = request.form['name']
        title = request.form['title']
        description = request.form['description']
        url = request.form['url']
        module = request.form['module']
        chapter = request.form['chapter']
        category = request.form['category']
        status = request.form['status']

        cursor.execute('INSERT INTO courses (name, title, description, url, chapter, module, category, status) values (?, ?, ?, ?, ?, ?, ?, ? ) RETURNING *', 
                        (name, title, description, url, module, chapter, category, status))

        new_course = cursor.fetchone()

        conn.commit()
        cursor.close()

        if conn is not None:
            conn.close()


        return jsonify({"message":"course created", "course":new_course}), 201

if __name__ == '__main__':
    app.run(debug = True)  