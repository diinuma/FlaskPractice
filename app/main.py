from flask import Flask, render_template, redirect, url_for, request
import psycopg2 as pg
from psycopg2.extras import DictCursor 

app = Flask(__name__)

# DB接続情報
DATABASE = {
    'host':'db',
    'dbname':'flaskdb',
    'user':'dbuser',
    'password':'dbuser',
    'port':5432
}

@app.route('/')
def todo_list():
    with pg.connect(**DATABASE) as connection, \
         connection.cursor(cursor_factory=DictCursor) as cursor:
        sql = """
            select * from todo
        """

        cursor.execute(sql)
        todos = cursor.fetchall()

    return render_template('list.html', title='TODOアプリ', todos=todos)


@app.route('/add')
def todo_add():
    return render_template('add.html', title='TODOアプリ')

@app.route('/add', methods=['POST'])
def add():
    with pg.connect(**DATABASE) as connection, \
         connection.cursor() as cursor:

        todo = request.form["todo"]
        sql = """
            insert into todo(todo) values(%(todo)s)
        """

        params = {
            'todo':todo
        }
        cursor.execute(sql, params)

    return redirect(url_for('todo_list'))

@app.route('/edit/<id>')
def todo_edit(id=None):
    with pg.connect(**DATABASE) as connection, \
        connection.cursor(cursor_factory=DictCursor) as cursor:
        sql = """
            select * 
            from todo
            where id = %(id)s
        """
        params = {
            'id':id
        }
        cursor.execute(sql, params)
        todo = cursor.fetchone()
    
    return render_template('edit.html', title='TODOアプリ', todo=todo)

@app.route('/edit', methods=['POST'])
def edit():
    with pg.connect(**DATABASE) as connection, \
         connection.cursor() as cursor:

        id = request.form['id']
        todo = request.form['todo']
        sql = """
            update todo 
            set todo = %(todo)s
            where id = %(id)s 
        """

        params = {
            'id':id,
            'todo':todo
        }
        cursor.execute(sql, params)

    return redirect(url_for('todo_list'))

@app.route('/', methods=['POST'])
def delete(id=None):
    with pg.connect(**DATABASE) as connection, \
         connection.cursor() as cursor:

        id = request.form['id']

        sql = """
            delete from todo
            where id = %(id)s 
        """

        params = {
            'id':id
        }
        cursor.execute(sql, params)

    return redirect(url_for('todo_list'))

# サーバーを実行する
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")