# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 10:29:09 2026

@author: User
"""

import sqlite3

conn = sqlite3.connect('students.db')

conn.execute("PRAGMA foreign_keys = ON;")

cursor = conn.cursor()
def print_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    print(f"\nTable: {table_name}")
    print(" | ".join(columns))
    print("-" * 30)

    for row in rows:
        print(" | ".join(str(value) for value in row))

#///////////////////////////////////////////////////////

cursor.execute("""
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name TEXT NOT NULL,
    age INT
)
""")

students = [
    (1, 'Alice', 20),
    (2, 'Bob', 22),
    (3, 'Charlie', 21)
]
cursor.executemany("INSERT INTO students VALUES (?, ?, ?)", students)

conn.commit()

print_table(cursor, "students")

#///////////////////////////////////////////////////////

cursor.execute("""
CREATE TABLE registered_Courses (
    student_id INT ,
    course_id INT NOT NULL,
    PRIMARY KEY(student_id, course_id),
    FOREIGN KEY(student_id ) references students(student_id)
    
)
""")

registrations = [
    (1, 101),
    (1, 102),
    (2, 101),
    (2, 103),
    (3, 102),
    (3, 103)
]
cursor.executemany("INSERT INTO registered_Courses VALUES (?, ?)", registrations)

conn.commit()

print_table(cursor, "registered_Courses")

#///////////////////////////////////////////////////////

cursor.execute("""
CREATE TABLE Grades (
    student_id INT ,
    course_id INT, 
    received_grade REAL,
    PRIMARY KEY(student_id, course_id),
    FOREIGN KEY(student_id,course_id ) references registered_Courses(student_id,course_id)
    
)
""")
grades = [
    (1, 101, 85.0),
    (1, 102, 90.0),
    (2, 101, 75.0),
    (2, 103, 80.0),
    (3, 102, 92.0),
    (3, 103, 95.0)
]
cursor.executemany("INSERT INTO Grades VALUES (?, ?, ?)", grades)

conn.commit()

print_table(cursor, "Grades")

#///////////////////////////////////////////////////////

cursor.execute("""
SELECT student_id, AVG(received_grade) 
FROM Grades 
GROUP BY student_id
""")
rows = cursor.fetchall()
for row in rows:
    print(f"Student ID: {row[0]}, Average Grade: {row[1]:.2f}")

#///////////////////////////////////////////////////////

cursor.execute("""
SELECT g.student_id, g.course_id, g.received_grade AS max_grade
From Grades g
JOIN(
     SELECT student_id, MAX(received_grade) AS max_grade
     FROM Grades
     GROUP BY student_id
     ) mg
ON g.student_id = mg.student_id AND g.received_grade = mg.max_grade
""")
rows = cursor.fetchall()

for row in rows:
    print(f"Student ID: {row[0]}, Course ID: {row[1]}, Max Grade: {row[2]}")
