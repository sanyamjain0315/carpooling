from google.cloud import firestore
from utility.util import *

service_account_json_path = "auth\\firebase_auth2.json"
db = firestore.Client.from_service_account_json(service_account_json_path, project=PROJECT2)

def append_to_existing_emails(email: str):
    if validate_email(email=email):
        doc_ref = db.collection(USERS).document("ExistingEmails")
        doc = doc_ref.get()
        existing_email_list = doc.to_dict().get('existing_email_list')
        print(existing_email_list)
        print(type(existing_email_list))
        if email in existing_email_list:
            return False
        else:
            existing_email_list.append(email)
            doc_ref.update({"existing_email_list": existing_email_list})
            return True
    else:
        return False
        


if append_to_existing_emails('sanyamjain0015@gmail.com'):
    print('added')
else:
    print("already present")




# def add_user(first_name:str, last_name, age, email, phone_number, gender, ocupation):
#     assert isinstance(first_name, str), 'first_name should be a String'
#     assert isinstance(last_name, str), 'last_name should be a String'
#     assert isinstance(email, str), 'email should be a String'
#     assert isinstance(phone_number, str), 'password should be a String'
#     assert isinstance(gender, str), 'admin status should be a Bool'    
#     assert isinstance(ocupation, int), 'admin status should be a Bool'
#     assert isinstance(age, int), 'admin status should be a Bool'


