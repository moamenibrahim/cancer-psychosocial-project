"""
Development phase script to empty dataset on firebase.

"""
import pyrebase

pyrebase_config = {
    "apiKey": "AIzaSyBIJYd5Xxa7DIORsLPJUCT2r4DqUa_bxlo",
    "authDomain": "analysis-820dc.firebaseapp.com",
    "databaseURL": "https://analysis-820dc.firebaseio.com",
    # projectId: "analysis-820dc",
    "storageBucket": "analysis-820dc.appspot.com",
    # messagingSenderId: "863565878024",
    "servicAccount": "./firebase-config/config.json"
}

firebase = pyrebase.initialize_app(pyrebase_config)
db = firebase.database()

# db.child("co-occurrences-all").remove()
