from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'db33edb0296bf8f4737c321c82d2103e933f333d50fb3ae9f1758002c3e0dc79'

@app.route("/", method=['GET', 'POST'])
def landing():
    return render_template("login.html")


if __name__ == '__main__':
    app.debug=True
    app.run(host='172.16.40.56', port=6969, debug=True)