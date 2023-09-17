import re, hashlib, random, string
from datetime import datetime as dt

USERS = 'Users'
INDIVIDUAL_USER = 'Individual_Users'
DRIVER_ROUTE = 'Driver_Route'
USER_ROUTE = 'User_Route'
PROJECT = 'blue-bebd1'
PROJECT2 = 'social-media-a6937'

sha256 = lambda input: hashlib.sha256(input.encode()).hexdigest()

def validate_email(email):  
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):  
        return True  
    return False  

class User():
    def __init__(self, first_name, last_name, age, email, mobile_number, gender, occupation, password, start_location, end_location, timing):
        assert isinstance(first_name, str), 'first_name should be a String'
        assert isinstance(last_name, str), 'last_name should be a String'
        assert isinstance(age, int), 'age should be a Integer'
        assert isinstance(email, str), 'email should be a String'
        assert isinstance(mobile_number, str), 'mobile_number should be a String'
        assert isinstance(gender, str), 'gender should be a String'
        assert isinstance(occupation, str), 'occupation should be a String'
        assert isinstance(password, str), 'password should be a String'
        assert isinstance(start_location, str), 'start_location should be a String'
        assert isinstance(end_location, str), 'emaend_locationil should be a String'
        assert isinstance(timing, str), 'timing should be a String'
        
        #Current time for extra info
        now = dt.now()
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.mobile_number = mobile_number
        self.gender = gender
        self.occupation = occupation
        self.password = sha256(password)
        self.created_at = now.strftime("%d/%m/%Y, %H:%M:%S")
        self.updated_at = now.strftime("%d/%m/%Y, %H:%M:%S")
        self.trip_info = {'start_location': start_location,
                          'end_location': end_location,
                          'timing': timing}

    def get_json(self):
        return {'first_name':self.first_name,
                'last_name':self.last_name,
                'age': self.age,
                'email': self.email,
                'mobile_number': self.mobile_number,
                'gender': self.gender,
                'occupation': self.occupation,
                'password': self.password,
                'created_at': self.created_at,
                'updated_at': self.updated_at,
                'trip_info': self.trip_info}


def profile_gen(doc, fare, distance_traveled):
    user_profile = f'''
        <div class="profile-card">
            <div class="profile-img">
                <img src="https://e7.pngegg.com/pngimages/550/997/png-clipart-user-icon-foreigners-avatar-child-face.png" alt="User 2">
            </div>
            <div class="profile-info">
                <h2>Name: {doc['first_name']}</h2>
                <p>Age: {doc['age']}</p>
                <p>Gender:{doc['gender']}</p>
                <p>Occupation: {doc['gender']}</p>
                <p>Timing: {doc['first_name']}</p>
                <p>Start Location: {doc['first_name']}</p>
                <p>End Location: {doc['first_name']}</p>
                <p>Distance Traveled: {distance_traveled}</p>
                <p>Fare: ₹{fare}</p>
            </div>
            <div class="profile-buttons">
                <button class="accept-button">Accept</button>
                <button class="reject-button">Reject</button>
                <button class="view-map-button">View Map</button>
            </div>
        </div>
        
        '''
    return user_profile