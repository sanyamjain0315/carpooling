from flask import Flask, render_template, request, session, redirect, url_for, flash
from firebase_db import new_email_ckeck, append_to_existing_emails, check_password

app = Flask(__name__)
app.secret_key = 'db33edb0296bf8f4737c321c82d2103e933f333d50fb3ae9f1758002c3e0dc79'

@app.route("/", methods=['GET', 'POST'])
def home():
    message = ''
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        if new_email_ckeck(email):
            message = '<h4 style="color: red;">Invalid Email</h4>'
            return render_template("login.html", message=message)
        else:
            if check_password(email, password):
                session['user_email'] = email
                return redirect(url_for("home"))
            else:
                message = '<h4 style="color: red;">Invalid Passsword</h4>'
                return render_template("login.html", message=message)
    else:
        return render_template("login.html", message=message)
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    # if request.method=='POST':
    #     message = '<a style="color: red;">Invalid Credentials<a>'
    #     return render_template("login.html", message=message)
    # else:
        message = ''
        return render_template("login.html", message=message)



@app.route("/home")
def logout():
    if 'user_email' not in session:
        return redirect(url_for("/"))
    else:
        return redirect(url_for("home"))


@app.route("/about")
def about():
    return render_template("about_us")

@app.route("/contact_us")
def contact():
    return render_template("contact_us") 

@app.route("/sign_up")
def signup():
    return render_template("sign_up") 



if __name__ == '__main__':
    app.debug=True
    app.run(host='172.16.40.56', port=6969, debug=True)
