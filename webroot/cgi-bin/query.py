#!/usr/bin/env python3

import cgi
import cgitb
import json
import pymysql

cgitb.enable()

def query_student(student_id):
    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="mysql",
            port=3306,
            database="school",
        )
        cursor = conn.cursor()

        query = "SELECT student_id, student_name, class FROM students WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            student_id, student_name, class_ = result
            return {
                "student_id": student_id,
                "student_name": student_name,
                "class": class_,
            }
        else:
            return {"error": "Student not found"}

    except pymysql.MySQLError as err:
        return {"error": str(err)}

print("Content-Type: application/json\n")

form = cgi.FieldStorage()
student_id = form.getvalue('student_id')

if student_id is not None:
    result = query_student(student_id)
else:
    result = {"error": "No student ID provided"}

print(json.dumps(result))