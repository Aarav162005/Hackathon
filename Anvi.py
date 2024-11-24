from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Anvi.html')

@app.route('/search', methods=['POST'])
def search():
    hospital_name = request.form['search']
    # Connect to the database and search for the hospital
    conn = sqlite3.connect('hospitals.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hospitals WHERE name LIKE ?", ('%' + hospital_name + '%',))
    results = cursor.fetchall()
    conn.close()
    if results:
        return render_template('Anvi.html', hospitals=results)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)