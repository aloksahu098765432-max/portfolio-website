from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# DATABASE CREATE
def init_db():

    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# HOME PAGE
@app.route('/')
def home():

    return render_template('index.html')

# CONTACT FORM
@app.route('/contact', methods=['POST'])
def contact():

    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO messages(name, email, message)
        VALUES (?, ?, ?)
    ''', (name, email, message))

    conn.commit()
    conn.close()

    return redirect('/')

# SHOW MESSAGES
@app.route('/messages')
def messages():

    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM messages')

    data = cursor.fetchall()

    conn.close()

    return render_template('messages.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)