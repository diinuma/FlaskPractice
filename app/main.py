from flask import Flask, render_template, redirect, url_for, request
import psycopg2 as pg
import psycopg2.extras

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
         connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
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
            insert into todo values(%(todo)s)
        """

        params = {
            'todo':todo
        }
        cursor.execute(sql, params)

    return redirect(url_for('todo_list'))

@app.route('/edit/<id>')
def todo_edit(id=None):
    with pg.connect(**DATABASE) as connection, \
        connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        sql = """
            select * 
            from todo
            where id = %(id)s
        """
        params = {
            'id':id
        }
        cursor.execute(sql, params)
        todos = cursor.fetchall()
    print(todos)
    return render_template('edit.html', title='TODOアプリ', todos=todos)

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

"""
@app.route('/')
def hello():
    name = "Hello World!!"
    with pg.connect(**DATABASE) as conn, conn.cursor() as cur:
        sql = """
            #select * 
            #from todo
            #where todo = %(todo)s
"""
        params = {
            'todo':'flaskapp'
        }
        cur.execute(sql, params)
        rows = cur.fetchall()

    return render_template('hello.html', title='flask test', name=name, rows=rows)

@app.route('/good')
def good():
    name = "Good"
    return render_template('good.html', title='flask test', val1="Good", val2="Bad")
"""

# サーバーを実行する
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")