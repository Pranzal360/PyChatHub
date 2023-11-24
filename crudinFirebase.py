from pyrebase import initialize_app
from time import time

config = {
    "apiKey": "AIzaSyCkej-bgiR6yLXqwoU-kc9uzN5RabXJcGM",
    "authDomain": "learningfirebase-13fb9.firebaseapp.com",
    "databaseURL": "https://learningfirebase-13fb9-default-rtdb.firebaseio.com",
    "projectId": "learningfirebase-13fb9",
    "storageBucket": "learningfirebase-13fb9.appspot.com",
    "messagingSenderId": "900385534931",
    "appId": "1:900385534931:web:03dad30335f27b12d7b526",
    "databaseURL": "https://learningfirebase-13fb9-default-rtdb.firebaseio.com/",
}


firebase = initialize_app(config=config)
auth = firebase.auth()

db = firebase.database()


def authenticate(email, password):
    start_time = time()
    user = auth.sign_in_with_email_and_password(email, password)
    print("upto here")
    uid = user["localId"]
    idtoken = user["idToken"]  # change with this refresh token or something
    refresh_token = user["refreshToken"]
    nameList = db.child("users").child(uid).get(token=idtoken).val()
    enttime = time()
    estd = enttime - start_time
    print(f"estd = {estd}")
    print(f"idtoken = {idtoken}")
    print(f"refreshtoken  = {idtoken}")

    return uid, nameList["username"], idtoken, refresh_token


def check_username(username, token):
    result = db.child("users").order_by_child("username").equal_to(username).get(token)

    if result.val() is not None and result.val() != []:
        print("oh, I am here too")
        print(result.val() is not None)

        return result.val() is not None  # returns true value xa vane
    else:
        return False  # natra flase # data xa vane true return garxa natra false


def create_user(email, password, username):

    user = auth.create_user_with_email_and_password(email, password)
    uid = user["localId"]
    token = user["idToken"]

    # make table with user name and email
    data = {"uid": uid, "username": username, "email": email}
    print(data)
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
