from flask import Flask, render_template



app = Flask(__name__)


# testing the initial setup
# will need to comment the code below out
@app.route('/')
def index():
    first_name = "Kenai"
    return render_template("index.html", first_name=first_name)
# end commented out code

# testing out returning a user
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name=name)
# end commented out code

# Custom Error Pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
        return render_template("404.html"), 404

# Internal Server Error
# Invalid URL
@app.errorhandler(500)
def page_not_found(e):
        return render_template("500.html"), 500

