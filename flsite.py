from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('base.html')

@app.route("/about")
def about():
    return render_template('base.html')

@app.route("/blog")
def blog():
    return render_template('base.html')

if __name__ == "__main__":
    app.run(debug=True)