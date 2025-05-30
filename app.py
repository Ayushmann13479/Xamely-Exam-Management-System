from flask import Flask, render_template, request, redirect, session
from db_config import get_db_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    role = request.form['role']
    username = request.form['username']
    password = request.form['password']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if role == 'admin':
        cursor.execute('SELECT * FROM admins WHERE username = %s', (username,))
        admin = cursor.fetchone()
        if admin and admin['password'] == password:
            session['role'] = 'admin'
            session['admin_id'] = admin['admin_id']
            session['username'] = admin['username']
            return redirect('/admin/dashboard')
        else:
            return render_template('login.html', error='Invalid admin credentials')
    elif role == 'student':
        cursor.execute('SELECT * FROM students WHERE email = %s', (username,))
        student = cursor.fetchone()
        if student and student['password'] == password:
            session['role'] = 'student'
            session['user_id'] = student['user_id']
            session['name'] = student['name']
            return redirect('/student/dashboard')
        else:
            return render_template('login.html', error='Invalid student credentials')
    else:
        return render_template('login.html', error='Invalid role selected')

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect('/')
    return render_template('admin_dashboard.html', username=session.get('username'))

@app.route('/student/dashboard')
def student_dashboard():
    if session.get('role') != 'student':
        return redirect('/')
    return render_template('student_dashboard.html', name=session.get('name'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/admin/students')
def admin_students():
    if session.get('role') != 'admin':
        return redirect('/')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    return render_template('students.html', students=students)

@app.route('/admin/students/add', methods=['GET', 'POST'])
def add_student():
    if session.get('role') != 'admin':
        return redirect('/')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        roll_number = request.form['roll_number']
        phone_number = request.form['phone_number']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO students (password, email, name, roll_number, phone_number) VALUES (%s, %s, %s, %s, %s)',
                       (password, email, name, roll_number, phone_number))
        conn.commit()
        conn.close()
        return redirect('/admin/students')
    return render_template('add_student.html')

@app.route('/admin/students/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_student(user_id):
    if session.get('role') != 'admin':
        return redirect('/')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        roll_number = request.form['roll_number']
        phone_number = request.form['phone_number']
        cursor2 = conn.cursor()
        cursor2.execute('UPDATE students SET email=%s, name=%s, roll_number=%s, phone_number=%s WHERE user_id=%s',
                       (email, name, roll_number, phone_number, user_id))
        conn.commit()
        conn.close()
        return redirect('/admin/students')
    cursor.execute('SELECT * FROM students WHERE user_id = %s', (user_id,))
    student = cursor.fetchone()
    conn.close()
    return render_template('edit_student.html', student=student)

@app.route('/admin/students/delete/<int:user_id>', methods=['POST'])
def delete_student(user_id):
    if session.get('role') != 'admin':
        return redirect('/')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE user_id = %s', (user_id,))
    conn.commit()
    conn.close()
    return redirect('/admin/students')

@app.route('/admin/subjects')
def admin_subjects():
    if session.get('role') != 'admin':
        return redirect('/')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM subjects')
    subjects = cursor.fetchall()
    conn.close()
    return render_template('subjects.html', subjects=subjects)

@app.route('/admin/subjects/add', methods=['GET', 'POST'])
def add_subject():
    if session.get('role') != 'admin':
        return redirect('/')
    if request.method == 'POST':
        subject_name = request.form['subject_name']
        credits = request.form['credits']
        teacher_name = request.form['teacher_name']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO subjects (subject_name, credits, teacher_name) VALUES (%s, %s, %s)',
                       (subject_name, credits, teacher_name))
        conn.commit()
        conn.close()
        return redirect('/admin/subjects')
    return render_template('add_subject.html')

@app.route('/admin/subjects/edit/<int:subject_id>', methods=['GET', 'POST'])
def edit_subject(subject_id):
    if session.get('role') != 'admin':
        return redirect('/')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        subject_name = request.form['subject_name']
        credits = request.form['credits']
        teacher_name = request.form['teacher_name']
        cursor2 = conn.cursor()
        cursor2.execute('UPDATE subjects SET subject_name=%s, credits=%s, teacher_name=%s WHERE subject_id=%s',
                        (subject_name, credits, teacher_name, subject_id))
        conn.commit()
        conn.close()
        return redirect('/admin/subjects')
    cursor.execute('SELECT * FROM subjects WHERE subject_id = %s', (subject_id,))
    subject = cursor.fetchone()
    conn.close()
    return render_template('edit_subject.html', subject=subject)

@app.route('/admin/subjects/delete/<int:subject_id>', methods=['POST'])
def delete_subject(subject_id):
    if session.get('role') != 'admin':
        return redirect('/')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM subjects WHERE subject_id = %s', (subject_id,))
    conn.commit()
    conn.close()
    return redirect('/admin/subjects')

@app.route('/admin/exams')
def admin_exams():
    if session.get('role') != 'admin':
        return redirect('/')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''SELECT exams.exam_id, exams.exam_link, students.name AS student_name, subjects.subject_name
                      FROM exams
                      JOIN students ON exams.user_id = students.user_id
                      JOIN subjects ON exams.subject_id = subjects.subject_id''')
    exams = cursor.fetchall()
    conn.close()
    return render_template('exams.html', exams=exams)

@app.route('/admin/exams/add', methods=['GET', 'POST'])
def add_exam():
    if session.get('role') != 'admin':
        return redirect('/')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT user_id, name FROM students')
    students = cursor.fetchall()
    cursor.execute('SELECT subject_id, subject_name FROM subjects')
    subjects = cursor.fetchall()
    if request.method == 'POST':
        user_id = request.form['user_id']
        subject_id = request.form['subject_id']
        exam_link = request.form['exam_link']
        cursor2 = conn.cursor()
        cursor2.execute('INSERT INTO exams (user_id, subject_id, exam_link) VALUES (%s, %s, %s)',
                        (user_id, subject_id, exam_link))
        conn.commit()
        conn.close()
        return redirect('/admin/exams')
    conn.close()
    return render_template('add_exam.html', students=students, subjects=subjects)

@app.route('/admin/exams/edit/<int:exam_id>', methods=['GET', 'POST'])
def edit_exam(exam_id):
    if session.get('role') != 'admin':
        return redirect('/')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT user_id, name FROM students')
    students = cursor.fetchall()
    cursor.execute('SELECT subject_id, subject_name FROM subjects')
    subjects = cursor.fetchall()
    if request.method == 'POST':
        user_id = request.form['user_id']
        subject_id = request.form['subject_id']
        exam_link = request.form['exam_link']
        cursor2 = conn.cursor()
        cursor2.execute('UPDATE exams SET user_id=%s, subject_id=%s, exam_link=%s WHERE exam_id=%s',
                        (user_id, subject_id, exam_link, exam_id))
        conn.commit()
        conn.close()
        return redirect('/admin/exams')
    cursor.execute('SELECT * FROM exams WHERE exam_id = %s', (exam_id,))
    exam = cursor.fetchone()
    conn.close()
    return render_template('edit_exam.html', exam=exam, students=students, subjects=subjects)

@app.route('/admin/exams/delete/<int:exam_id>', methods=['POST'])
def delete_exam(exam_id):
    if session.get('role') != 'admin':
        return redirect('/')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM exams WHERE exam_id = %s', (exam_id,))
    conn.commit()
    conn.close()
    return redirect('/admin/exams')

@app.route('/student/exams')
def student_exams():
    if session.get('role') != 'student':
        return redirect('/')
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''SELECT exams.exam_id, exams.exam_link, subjects.subject_name
                      FROM exams
                      JOIN subjects ON exams.subject_id = subjects.subject_id
                      WHERE exams.user_id = %s''', (user_id,))
    exams = cursor.fetchall()
    conn.close()
    return render_template('student_exams.html', exams=exams)

if __name__ == '__main__':
    app.run(debug=True) 