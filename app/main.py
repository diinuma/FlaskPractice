from flask import Flask, render_template
import psycopg2 as pg

app = Flask(__name__)

DATABASE = {
    'host':'db',
    'dbname':'flaskdb',
    'user':'dbuser',
    'password':'dbuser',
    'port':5432
}

@app.route('/')
def hello():
    name = "Hello World!!"
    with pg.connect(**DATABASE) as conn, conn.cursor() as cur:
        sql = """
            select * 
            from todo
            where todo = %(todo)s
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

# サーバーを実行する
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")