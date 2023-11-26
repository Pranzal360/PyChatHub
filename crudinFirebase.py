from pyrebase import initialize_app
from time import time

config = {
    "apiKey": "***REMOVED***",
    "authDomain": "***REMOVED***",
    "databaseURL": "***REMOVED***",
    "projectId": "***REMOVED***",
    "storageBucket": "***REMOVED***.appspot.com",
    "messagingSenderId": "***REMOVED***",
    "appId": "1:***REMOVED***:web:03dad30335f27b12d7b526",
    "databaseURL": "***REMOVED***/",
}


firebase = initialize_app(config=config)
auth = firebase.auth()

db = firebase.database()


def authenticate(email, password):
    start_time = time()
    user = auth.sign_in_with_email_and_password(email, password)
    print("auth completed from database file")
    uid = user["localId"]
    idtoken = user["idToken"]  # change with this refresh token or something
    refresh_token = user["refreshToken"]
    nameList = db.child("users").child(uid).get(token=idtoken).val()
    enttime = time()
    estd = enttime - start_time
    print(f"estd = {estd}")


    return uid, nameList["username"], idtoken, refresh_token


def check_username(username, token):
    result = db.child("users").order_by_child("username").equal_to(username).get(token)

    if result.val() is not None and result.val() != []:


        return result.val() is not None  # returns true value xa vane
    else:
        return False  # natra flase # data xa vane true return garxa natra false


def create_user(email, password, username):

    user = auth.create_user_with_email_and_password(email, password)
    uid = user["localId"]
    token = user["idToken"]

    # make table with user name and email
    data = {"uid": uid, "username": username, "email": email}

    # now check if there's valid username ..
    if check_username(username, token):  # gets true if data xa vane
        user = auth.delete_user_account(token)
        return False
    else:
        db.child("users").child(uid).set(data, token)
        return True


def get_refresh_token(refresh_token):
    time1 = time()
    usertoken = auth.refresh(refresh_token)
    end_time = time()
    elp = end_time - time1
    print(f"runtime {elp}")
    return usertoken["idToken"]


def logout(e):
    print("logoout ran")
    auth.current_user = None

def reset_pwd(email):
    try:
        res = auth.send_password_reset_email(email)
        print(res)
    except Exception as e:
        print(e)