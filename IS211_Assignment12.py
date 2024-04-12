from flask import Flask, request, redirect, render_template, session, g
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = 'hw13.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'password':
            error = 'Invalid credentials'
        else:
            session['logged_in'] = True
            return redirect('/dashboard')
    return render_template('login.html', error=error)
    
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/login')
    db = get_db()
    students_cur = db.execute('SELECT * FROM students')
    students = students_cur.fetchall()
    quizzes_cur = db.execute('SELECT * FROM quizzes')
    quizzes = quizzes_cur.fetchall()

    print("Students:", students)
    print("Quizzes:", quizzes)

    return render_template('dashboard.html', students=students, quizzes=quizzes)

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        db = get_db()
        db.execute('INSERT INTO students (first_name, last_name) VALUES (?, ?)',
                   [request.form['first_name'], request.form['last_name']])
        db.commit()
        return redirect('/dashboard')
    return render_template('add_student.html')

@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'POST':
        db = get_db()
        db.execute('INSERT INTO quizzes (subject, question_count, date_given) VALUES (?, ?, ?)',
               [request.form['subject'], request.form['question_count'], request.form['date_given']])
        db.commit()
        return redirect('/dashboard')
    return render_template('add_quiz.html')

if __name__ == '__main__':
    app.run(debug=True)