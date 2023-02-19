"""
Development phase script to empty dataset on firebase.

"""
import pyrebase

pyrebase_config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "storageBucket": ",
    "servicAccount": ""
}

firebase = pyrebase.initialize_app(pyrebase_config)
db = firebase.database()
# db.child("co-occurrences-all").remove()
