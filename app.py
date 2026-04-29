from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def db():
    conn = sqlite3.connect('cms.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    conn = db()
    total = conn.execute("select count(*) from students").fetchone()[0]
    conn.close()
    return render_template('dashboard.html', total=total)

@app.route('/students')
def students():
    conn = db()
    data = conn.execute("select * from students").fetchall()
    conn.close()
    return render_template('students.html', students=data)

@app.route('/add_student', methods=['GET','POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        dept = request.form['dept']

        conn = db()
        conn.execute("insert into students(name,roll,dept) values(?,?,?)",(name,roll,dept))
        conn.commit()
        conn.close()

        return redirect('/students')

    return render_template('add_student.html')

@app.route('/attendance')
def attendance():
    return render_template('attendance.html')

@app.route('/marks')
def marks():
    return render_template('marks.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)