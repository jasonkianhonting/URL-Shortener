#############################################################
# Author = Jason (Kian Hon Ting)
# Github = https://github.com/jasonkianhonting
############################################################


from flask import Flask, render_template, request, url_for, redirect
from helpers import *

app = Flask(__name__)

# Declaring all the routes available


@app.route('/home')
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        userEmail = request.form['Email']
        userPass = request.form['Password']
        # If login is valid, redirects to convert page, otherwise stays at the same page with error message pop ups
        if login(userEmail, userPass) == True:
            return redirect(url_for('convert'))
        else:
            return render_template("frontpage.html", messages={"Incorrect Username or Password, Please try again"})
    return render_template("frontpage.html")

# Allows users to use the convert function


@app.route('/convert', methods=['POST', 'GET'])
@required_login
def convert():
    if request.method == 'POST':
        userLink = request.form['URL']
        newLink = shorten(userLink)
        return render_template("convert.html", messages={newLink})
    return render_template("convert.html")

# Allows users to logout successfully


@app.route('/logout')
@required_login
def logout():
    Logout()
    return redirect(url_for('home'))


@app.errorhandler(404)
def not_found(e):
    return render_template("error404.html"), 404


# Starts the application
if __name__ == '__main__':
    app.run(debug=True)
