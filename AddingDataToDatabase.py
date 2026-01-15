import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : "https://votingdetectorsystem-default-rtdb.firebaseio.com/"
})

ref = db.reference('Voters')
data = {
    "212954":
        {
            "name": "Manav Manoj",
            "major": "Data Science",
            "starting_year": 2021,
            "voting_done": 0,
            "roll_no": 4,
            "year": 3,
            "voting_time": "2022-12-11 00:54:34"
        },
    "212955":
        {
            "name": "Sreelekshman",
            "major": "Data Science",
            "starting_year": 2021,
            "voting_done": 0,
            "roll_no": 5,
            "year":  3,
            "voting_time": "2022-12-11 00:54:34"
        },
    "212956":
        {
            "name": "Neha Rashi",
            "major": "Data Science",
            "starting_year": 2021,
            "voting_done": 0,
            "roll_no": 6,
            "year": 3,
            "voting_time": "2022-12-11 00:54:34"
        },
    "212958":
        {
            "name": "Aleena V M",
            "major": "Data Science",
            "starting_year": 2021,
            "voting_done": 0,
            "roll_no": 7,
            "year": 3,
            "voting_time": "2022-12-11 00:54:34"
        },
    "212959":
        {
            "name": "Farhan",
            "major": "Data Science",
            "starting_year": 2021,
            "voting_done": 0,
            "roll_no": 8,
            "year": 3,
            "voting_time": "2022-12-11 00:54:34"
        },
    "212961":
        {
            "name": "Bright Lee",
            "major": "Data Science",
            "starting_year": 2021,
            "voting_done": 0,
            "roll_no": 10,
            "year": 3,
            "voting_time": "2022-12-11 00:54:34"
        },
    "212962":
        {
            "name": "Bincy Manuel",
            "major": "Data Science",
            "starting_year": 2021,
            "voting_done": 0,
            "roll_no": 11,
            "year": 3,
            "voting_time": "2022-12-11 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)