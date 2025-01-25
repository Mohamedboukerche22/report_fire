from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

# إنشاء قاعدة البيانات
def init_db():
    conn = sqlite3.connect('reports.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            note TEXT,
            phone TEXT
        )
    ''')
    conn.commit()
    conn.close()

# الصفحة الرئيسية لتقديم البلاغ
@app.route('/', methods=['GET', 'POST'])
def report_fire():
    if request.method == 'POST':
        location = request.form['location']
        note = request.form['note']
        phone = request.form['phone']
        # إدخال البيانات في قاعدة البيانات
        conn = sqlite3.connect('reports.db')
        c = conn.cursor()
        c.execute('INSERT INTO reports (location, note, phone) VALUES (?, ?, ?)', (location, note, phone))
        conn.commit()
        conn.close()
        return "تم إرسال البلاغ بنجاح!"
    return render_template('report.html')

# صفحة الحماية المدنية لعرض البلاغات
@app.route('/admin')
def view_reports():
    conn = sqlite3.connect('reports.db')
    c = conn.cursor()
    c.execute('SELECT * FROM reports')
    reports = c.fetchall()
    conn.close()
    return render_template('admin.html', reports=reports)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

