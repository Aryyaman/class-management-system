import sqlite3
import os

if os.path.exists('cms.db'):
    os.remove('cms.db')

conn = sqlite3.connect('cms.db')
c = conn.cursor()

# Create Users table
c.execute('''
CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT
)
''')

# Create Students table
c.execute('''
CREATE TABLE students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll TEXT UNIQUE NOT NULL,
    dept TEXT
)
''')

# Create Courses table
c.execute('''
CREATE TABLE courses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL
)
''')

# Create Attendance table
c.execute('''
CREATE TABLE attendance(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    date TEXT NOT NULL,
    status TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id)
)
''')

# Create Marks table
c.execute('''
CREATE TABLE marks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    marks INTEGER,
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(course_id) REFERENCES courses(id)
)
''')

# Seed Dummy Data
c.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
c.execute("INSERT INTO users (username, password, role) VALUES ('teacher', 'teacher123', 'teacher')")

students = [
    ('Alice Smith', 'CS01', 'Computer Science'),
    ('Bob Johnson', 'CS02', 'Computer Science'),
    ('Charlie Brown', 'EE01', 'Electrical Engineering'),
    ('Diana Ross', 'ME01', 'Mechanical Engineering')
]
c.executemany("INSERT INTO students (name, roll, dept) VALUES (?, ?, ?)", students)

courses = [
    ('CS101', 'Intro to Programming'),
    ('EE101', 'Basic Electronics'),
    ('ME101', 'Engineering Mechanics')
]
c.executemany("INSERT INTO courses (code, name) VALUES (?, ?)", courses)

# Add some attendance and marks for dummy data presentation
c.execute("INSERT INTO attendance (student_id, date, status) VALUES (1, '2023-10-01', 'Present')")
c.execute("INSERT INTO attendance (student_id, date, status) VALUES (2, '2023-10-01', 'Absent')")
c.execute("INSERT INTO marks (student_id, course_id, marks) VALUES (1, 1, 95)")
c.execute("INSERT INTO marks (student_id, course_id, marks) VALUES (2, 1, 88)")

conn.commit()
conn.close()

print("Database created and seeded successfully.")