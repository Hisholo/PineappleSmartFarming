import pyrebase

def Connect():
    config = {
        "apiKey": "AIzaSyA0PyB83EFWawsDt7xQ9IkwSIo8HaljDLY",
        "authDomain": "pineapple-smart-farming.firebaseapp.com",
        "databaseURL": "https://pineapple-smart-farming-default-rtdb.firebaseio.com",
        "projectId": "pineapple-smart-farming",
        "storageBucket": "pineapple-smart-farming.appspot.com",
        "messagingSenderId": "801877999980",
        "appId": "1:801877999980:web:510b75804517340044b349",
        "measurementId": "G-JPCJ2EETKW"
    }
    return pyrebase.initialize_app(config)