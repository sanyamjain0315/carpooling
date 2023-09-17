from flask import Flask, render_template, request, session, redirect, url_for, flash
from firebase_db import *
import polyline
# import razorpay
from datetime import datetime
from models.route_calculations import call_directions,Route_functions

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


@app.route("/about_us")
def about():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    else:
        return render_template("about_us.html")

@app.route("/contact_us")
def contact():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    else:
        return render_template("contact_us.html") 

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

@app.route("/data_collection")
def data_collection():
    if 'user_email' in session:
        return render_template("data_collection.html")
    else:
        session.pop('user_email',None) 
        return render_template("login.html")
    

@app.route("/add_passenger", methods=['POST'])
def add_passenger():
    if 'user_email' in session:
        start_location = request.form['start_location']
        end_location = request.form['end_location']
        timing = request.form['timing']
        api_output = call_directions(start=start_location, end=end_location,time=timing)
        add_passenger_routes(session['user_email'], api_output)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route("/add_driver", methods=['POST'])
def add_driver():
    if 'user_email' in session:
        start_location = request.form['start_location']
        end_location = request.form['end_location']
        timing = request.form['timing']
        empty_seats = request.form['empty_seats']
        car_type = request.form['car_type']
        fuel_type = request.form['fuel_type']
        
        api_output = call_directions(start=start_location,end=end_location,time=timing)
        add_driver_routes(session['user_email'], api_output, empty_seats, car_type, fuel_type)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))
    
@app.route("/connect")
def connect():
    if 'user_email' in session:
        doc_ref = ref_driver_route.document(session['user_email'])

        doc = doc_ref.get()
        if doc.exists:
            doc = doc.to_dict()
            driver_polyline = polyline.decode(doc['google_maps_output']['overview_polyline']['points'])
            driver_polyline  =[(round(lat, 3), round(lon, 3)) for lat, lon in driver_polyline]

            docs = ref_passenger_route.stream()
            pass_route = []
            for doc in docs:
                pass_route.append({'polyline':[(round(lat, 3), round(lon, 3)) for lat, lon in polyline.decode(doc.to_dict()['google_maps_output']['overview_polyline']['points'])] ,
                                   'email': doc.id,
                                   'doc': doc.to_dict()})
                print(doc.to_dict())

            final_data =[]
            for passenger_route in pass_route:
                obj = Route_functions()
                cost = obj.route_similarity(driver_polyline,passenger_route['polyline'])
                final_data.append([ cost, session['user_email'], passenger_route['email'], driver_polyline, passenger_route['polyline'], passenger_route['doc']])
                del obj

            final_data = sorted(final_data, key=lambda x: x[0])
            # temp = []
            # for i in final_data:
            #     temp.append
            return render_template("connect.html", match=final_data)
        else:
            return redirect(url_for('home'))

        return render_template("login.html")
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.debug=True
    app.run(host='172.16.40.56', port=6969, debug=True)
