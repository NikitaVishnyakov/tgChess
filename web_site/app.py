from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return "about page"

@app.route('/about/<string:name>/<int:id>')
def user_page(name, id):
    return "User page " + name + " - " + str(id)

if __name__ == "__main__":
    app.run(debug=True)