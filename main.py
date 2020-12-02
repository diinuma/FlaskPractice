from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    name = "Hello World"
    return render_template('hello.html', title='flask test', name=name)

@app.route('/good')
def good():
    name = "Good"
    return render_template('good.html', title='flask test', val1="Good", val2="Bad")

# サーバーを実行する
if __name__ == "__main__":
    app.run(debug=True)