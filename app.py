from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super_secret_key_cms'

def db():
    conn = sqlite3.connect('cms.db')
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = db()
        user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = db()
    total_students = conn.execute("SELECT count(*) FROM students").fetchone()[0]
    
    # Calculate average attendance
    attendance_count = conn.execute("SELECT count(*) FROM attendance").fetchone()[0]
    present_count = conn.execute("SELECT count(*) FROM attendance WHERE status='Present'").fetchone()[0]
    avg_attendance = round((present_count / attendance_count * 100) if attendance_count > 0 else 0)
    
    # Calculate average marks
    avg_marks_row = conn.execute("SELECT avg(marks) FROM marks").fetchone()[0]
    avg_marks = round(avg_marks_row) if avg_marks_row else 0
    
    conn.close()
    return render_template('dashboard.html', total=total_students, avg_attendance=avg_attendance, avg_marks=avg_marks)

@app.route('/students')
@login_required
def students():
    conn = db()
    data = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template('students.html', students=data)

@app.route('/add_student', methods=['GET','POST'])
@login_required
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        dept = request.form['dept']

        conn = db()
        try:
            conn.execute("INSERT INTO students(name,roll,dept) VALUES(?,?,?)", (name,roll,dept))
            conn.commit()
            flash('Student added successfully!', 'success')
        except sqlite3.IntegrityError:
            flash('Roll number already exists!', 'error')
        conn.close()

        return redirect(url_for('students'))

    return render_template('add_student.html')

@app.route('/delete_student/<int:id>', methods=['POST'])
@login_required
def delete_student(id):
    conn = db()
    conn.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Student deleted.', 'success')
    return redirect(url_for('students'))

@app.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    conn = db()
    date = request.args.get('date') or request.form.get('date')
    
    if request.method == 'POST':
        date = request.form['date']
        for key, value in request.form.items():
            if key.startswith('status_'):
                student_id = key.split('_')[1]
                exists = conn.execute("SELECT id FROM attendance WHERE student_id=? AND date=?", (student_id, date)).fetchone()
                if exists:
                    conn.execute("UPDATE attendance SET status=? WHERE id=?", (value, exists['id']))
                else:
                    conn.execute("INSERT INTO attendance (student_id, date, status) VALUES (?,?,?)", (student_id, date, value))
        conn.commit()
        flash('Attendance saved.', 'success')
        
    students = conn.execute("SELECT * FROM students").fetchall()
    
    attendance_data = {}
    if date:
        records = conn.execute("SELECT student_id, status FROM attendance WHERE date=?", (date,)).fetchall()
        attendance_data = {r['student_id']: r['status'] for r in records}
        
    conn.close()
    return render_template('attendance.html', students=students, date=date, attendance_data=attendance_data)

@app.route('/marks', methods=['GET', 'POST'])
@login_required
def marks():
    conn = db()
    course_id = request.args.get('course_id') or request.form.get('course_id')
    
    if request.method == 'POST':
        course_id = request.form['course_id']
        for key, value in request.form.items():
            if key.startswith('marks_') and value:
                student_id = key.split('_')[1]
                exists = conn.execute("SELECT id FROM marks WHERE student_id=? AND course_id=?", (student_id, course_id)).fetchone()
                if exists:
                    conn.execute("UPDATE marks SET marks=? WHERE id=?", (value, exists['id']))
                else:
                    conn.execute("INSERT INTO marks (student_id, course_id, marks) VALUES (?,?,?)", (student_id, course_id, value))
        conn.commit()
        flash('Marks saved.', 'success')
        
    courses = conn.execute("SELECT * FROM courses").fetchall()
    students = conn.execute("SELECT * FROM students").fetchall()
    
    marks_data = {}
    if course_id:
        records = conn.execute("SELECT student_id, marks FROM marks WHERE course_id=?", (course_id,)).fetchall()
        marks_data = {r['student_id']: r['marks'] for r in records}
        
    conn.close()
    return render_template('marks.html', courses=courses, students=students, course_id=int(course_id) if course_id else None, marks_data=marks_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)