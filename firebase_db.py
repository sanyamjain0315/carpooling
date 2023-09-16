from google.cloud import firestore
from utility.util import *

service_account_json_path = "auth\\firebase_auth2.json"
db = firestore.Client.from_service_account_json(service_account_json_path, project=PROJECT2)

ref_existing_email = db.collection(USERS).document("ExistingEmails")
ref_individual_user = db.collection(INDIVIDUAL_USER)

def new_email_ckeck(email):
    if validate_email(email=email):
        docs = ref_existing_email.get()
        existing_email_list = docs.to_dict().get('existing_email_list')
        if email not in existing_email_list:
            return True
        else:
            return False
    else:
        return False

def check_password(email,password):
    docs = ref_individual_user.document(email).get()
    encrypted_password = docs.to_dict().get('password')
    if encrypted_password == sha256(password):
         return True
    else:
        return False

def append_to_existing_emails(email: str):
        docs = ref_existing_email.get()
        existing_email_list = docs.to_dict().get('existing_email_list')
        existing_email_list.append(email)
        ref_existing_email.update({"existing_email_list": existing_email_list})    
        print(f"{email} added succesfully")    


def create_account(first_name, last_name, age, email, mobile_number, gender, occupation, password, start_location, end_location, timing):
    try:
        new_user = User(first_name=first_name, last_name=last_name, age=age, email=email, mobile_number=mobile_number, gender=gender, 
                        occupation=occupation, password=password, start_location=start_location, end_location=end_location, timing=timing)
        ref_individual_user.document(email).set(new_user.get_json())
        del new_user
        return True
    except:
        return False
     

# e = "naresh@abc.com"
# create_account(first_name='Naresh', last_name='Gusain', age=20, mobile_number='7977797788', gender="Male", occupation='Student', password='qwertyuiop', start_location='a', end_location='b', timing='123', email=e)
# append_to_existing_emails(email=e)
# def add_user(first_name:str, last_name, age, email, phone_number, gender, ocupation):
#     assert isinstance(first_name, str), 'first_name should be a String'
#     assert isinstance(last_name, str), 'last_name should be a String'
#     assert isinstance(email, str), 'email should be a String'
#     assert isinstance(phone_number, str), 'password should be a String'
#     assert isinstance(gender, str), 'admin status should be a Bool'    
#     assert isinstance(ocupation, int), 'admin status should be a Bool'
#     assert isinstance(age, int), 'admin status should be a Bool'


