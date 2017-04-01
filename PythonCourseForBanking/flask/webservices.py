from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def display_hello():
    # return jsonify(result='hello world')
    return render_template('test.html')


@app.route('/hello2')
def display_hello_2():
    return jsonify(result='hello again world!')


if __name__ == '__main__':
    app.run()
