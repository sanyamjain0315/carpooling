from flask import Flask, render_template, request, session, redirect, url_for, flash
from firebase_db import new_email_ckeck, append_to_existing_emails, check_password, create_account
import razorpay
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'db33edb0296bf8f4737c321c82d2103e933f333d50fb3ae9f1758002c3e0dc79'

@app.route("/", methods=['GET', 'POST'])
def login():
    message = ''
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        if new_email_ckeck(email):
            message = '<h4 style="color: red;">Invalid Email</h4>'
            session.pop('user_email',None) 
            return render_template("login.html", message=message)
        else:
            if check_password(email, password):
                session['user_email'] = email
                return redirect(url_for('home'))
            else:
                message = '<h4 style="color: red;">Invalid Passsword</h4>'
                session.pop('user_email',None) 
                return render_template("login.html", message=message)
    else:
        if 'user_email' in session:
            return redirect(url_for('home'))
        else:
            return render_template("login.html", message=message)


@app.route("/home")
def home():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    else:
        return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about_us")

@app.route("/contact_us")
def contact():
    return render_template("contact_us") 

@app.route("/sign_up", methods=['GET', 'POST'])
def signup():
    message = ''
    if request.method=='POST':
        if 'user_email' in session:
            session.pop('user_email',None) 
        email = request.form['email']
        if new_email_ckeck(email=email):
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            age = int(request.form['age'])
            mobile_number = request.form['mobile_number']
            gender = request.form['gender']
            occupation = request.form['occupation']
            password = request.form['password']
            start_location = request.form['start_location']
            end_location = request.form['end_location']
            timing = request.form['timing']
            
            for i in [first_name,last_name,age,mobile_number,gender,occupation,password,start_location,end_location,timing]:
                print(type(i))

            print(first_name,last_name,age,mobile_number,gender,occupation,password,start_location,end_location,timing)
            flag = create_account(first_name=first_name, last_name=last_name, age=age, email=email, mobile_number=mobile_number, gender=gender, occupation=occupation, 
                                  password=password, start_location=start_location, end_location=end_location, timing=timing)
            if flag:
                session['user_email'] = email
                append_to_existing_emails(email=email)
                return redirect(url_for('home'))
            else:
                return render_template("error.html")
        else:
            message = '<h3 style="color: red;">Email Already Exist</h3>'
            return render_template("sign_up.html", message=message) 
    else:
        return render_template("sign_up.html", message=message) 

@app.route("/logout")
def logout():
    session.pop('user_email',None) 
    return render_template("login.html")

@app.route("/pay", methods=['POST'])
def pay():
    global payment, name
    name = request.form.get('username')
    # client = razorpay.Client(auth=("RAZORPAY_ID", "RAZORPAY_SECRET"))
    client = razorpay.Client(auth=("rzp_test_bEmrlWMc2mxFJq", "NDkpNo7sfBHSFB5MGiKonRqG"))

    data = { "amount": 1, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    return render_template('pay.html', payment=payment)



if __name__ == '__main__':
    app.debug=True
    app.run(host='172.16.40.56', port=6969, debug=True)
