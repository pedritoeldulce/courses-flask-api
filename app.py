from flask import Flask, request, jsonify
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
def courses():

    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        
        cursor = conn.execute("SELECT * FROM courses")

        courses = [
            dict(id = row[0], name=row[1], title=row[2], description=row[3], url=row[4], module=row[5], chapter=row[6], category=row[7], status=row[8] )
            for row in cursor.fetchall()
        ]
        #courses = cursor.fetchall()

        if courses:
            return jsonify({"courses":courses}), 200

        return jsonify({"messaje":"Nothign found"}), 400

    if request.method == 'POST':

        name = request.form['name']
        title = request.form['title']
        description = request.form['description']
        url = request.form['url']
        module = request.form['module']
        chapter = request.form['chapter']
        category = request.form['category']
        status = request.form['status']

        print(title, module, chapter, type(module), type(int(module)))
        #vamos a verificar si hay un repetido
        cursor.execute('SELECT * FROM courses WHERE title=? AND url=? AND module=? AND chapter=?',
                        (title, url, int(module), int(chapter)))
                        
        course_repetido = cursor.fetchone()
        print(course_repetido)
        # verificar si conn hace falta cerrar para la consuilta de repetidp
        if course_repetido:
                 
            return jsonify({"message":"Bad request, Course Repeated"}), 400

        else:
            cursor.execute('INSERT INTO courses (name, title, description, url, module, chapter, category, status) values (?, ?, ?, ?, ?, ?, ?, ? ) RETURNING *', 
                        (name, title, description, url, module, chapter, category, status))

            new_course = cursor.fetchone()
            conn.commit()

        return jsonify({"message":"course created", "course":new_course}), 201

    
    cursor.close()

    if conn is not None:
            conn.close()

@app.route('/courses/<int:id>', methods=["GET", "PUT","DELETE"])
def get_course(id):

    conn = db_connection()
    cursor = conn.cursor()


    if request.method == "GET":
        course_found = None
        cursor.execute('SELECT * FROM courses WHERE id = ?',(id,))
        
        course_found = [
            dict(id = row[0], name=row[1], title=row[2], description=row[3], url=row[4], module=row[5], chapter=row[6], category=row[7], status=row[8] )
            for row in cursor.fetchall()
            ]

        if course_found:
            return jsonify({"message":"course found", "course":course_found}), 200
        return jsonify({"message":"not found"}), 400

    if request.method == "PUT":
        course_updated = None
        cursor.execute('UPDATE courses SET name=?, title=?, description=?, url=?, module=?, chapter=?, category=?, status=? WHERE id=? RETURNING *', 
                (request.form['name'], request.form['title'], request.form['description'], request.form['url'], request.form['module'], 
                    request.form['chapter'], request.form['category'], request.form['status'], id))
        
        course_updated = cursor.fetchone()
        conn.commit()

        if course_updated:
            return jsonify({"message":"course updated", "course": course_updated}), 200

        return jsonify({"message":"not found"}), 400

    if request.method == "DELETE":
        course_deleted = None

        cursor.execute('DELETE FROM courses WHERE id = ? RETURNING *', (id,))
        course_deleted = cursor.fetchone()
        conn.commit()

        if course_deleted:
            return jsonify({"message":"course deleted", "course":course_deleted}), 200
        return jsonify({"message":"not found"}), 400 

    cursor.close()  
    if conn is not None:
        conn.close()

if __name__ == '__main__':
    app.run(debug = True)  