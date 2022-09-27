import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash, session
import logging
from werkzeug.exceptions import abort
# from flask_session import Session
import sys 
from datetime import datetime
 
db_connection_count = 0

def log(x): 
    stdout_fileno = sys.stdout
    now = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    stdout_fileno.write('INFO:app:' + str(now) +', ' + str(x) + ' \n')

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    # session["db_connection_count"] = session["db_connection_count"] + 1

    f = open("db_connection_count.txt", "r")
    db_connection_count = int(float(f.read()))
    f.close()

    f = open("db_connection_count.txt", "w")
    db_connection_count = db_connection_count  + 1
    f.write(str(db_connection_count))
    f.close()

    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your secret key'
# app.config['SESSION_TYPE'] = 'filesystem'
# Session(app)

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        log('Article not found')
        return render_template('404.html'), 404
    else:
        log('Article "' + str(post['title']) + '" retrieved!')
        return render_template('post.html', post=post)


@app.route('/healthz')
def healthz():
    return 'OK'

@app.route('/metrics')
def metrics():
    f = open("db_connection_count.txt", "r")
    db_connection_count = f.read()
    f.close()
    connection = get_db_connection()
    posts = connection.execute('SELECT count(*) as count FROM posts').fetchall()
    return '{"db_connection_count": ' + str(db_connection_count) +' , "post_count": ' + str(posts[0]['count']) + '}'

# Define the About Us page
@app.route('/about')
def about():
    log('The "About Us" page is retrieved.')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            log('A new article is created. [' + title + ']')
            return redirect(url_for('index'))

    return render_template('create.html')

# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
