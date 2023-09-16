import re  

USERS = 'Users'
PROJECT = 'blue-bebd1'
PROJECT2 = 'social-media-a6937'
  
def validate_email(email):  
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):  
        return True  
    return False  