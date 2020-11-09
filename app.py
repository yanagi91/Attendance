from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/identify/<taikin>', methods=(['GET', 'POST']))
def main(taikin=None):
    return render_template('identify.html', taikin=taikin)


@app.route('hoge', method=(['GET', 'POST']))
def result():
    return


if __name__ == '__main__':
    app.run(debug=True)