from flask import Flask, render_template, request, redirect, url_for
import sqlite3

x = sqlite3.connect('task_manager.db')
cursor = x.cursor()
cursor.execute(''' CREATE TABLE IF NOT EXISTS tasks(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               description TEXT,
               due_date TEXT NOT NULL)
                ''')
x.commit()
x.close()

app = Flask(__name__)

#home page
@app.route('/')
def home():
    x = sqlite3.connect('task_manager.db')
    cursor = x.cursor()
    cursor.execute('SELECT * FROM tasks')
    t = cursor.fetchall()
    x.close()
    return render_template('index.html', tasks = t)

#add_task
@app.route('/add_task', methods=['POST','GET'])
def add():
    if request.method == 'POST':
        n = request.form['name']
        a = request.form['description']
        d = request.form['date']

        x = sqlite3.connect('task_manager.db')
        cursor = x.cursor()
        cursor.execute(f"INSERT INTO tasks(name, description, due_date) VALUES ('{n}', '{a}', '{d}')")
        x.commit()
        x.close()
        return redirect('/')
    return render_template('/add_task')

#delete_button
@app.route('/delete/<int:task_id>', methods=['POST']) 
def delete_tasks(task_id):
    x = sqlite3.connect('task_manager.db')
    cursor = x.cursor()
    cursor.execute(f'DELETE FROM tasks WHERE id = {task_id}')
    x.commit()
    x.close()
    return redirect(url_for('home'))

#go_to_add_page
@app.route("/add_task_page")
def add_page():
    return render_template("add_task.html")

if __name__ == "__main__":
    app.run(debug=True)
