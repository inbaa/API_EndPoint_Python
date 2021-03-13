import pyrebase

# Initialize Firebase
firebaseConfig = {
    "apiKey": "AIzaSyBzmB5NCWo9q8OiPtXva5JlAx4L8",
    "authDomain": "api-endpoint-edc.firebaseapp.com",
    "databaseURL": "https://api-endpoint-edc-default-rtdb.firebaseio.com",
    "projectId": "api-endpoint-edc0a",
    "storageBucket": "api-endpoint-edc.appspot.com",
    "messagingSenderId": "6072984808",
    "appId": "1:607112984808:web:ce6a28ed9b0c315d",
    "measurementId": "G-YBXCF6DDBV"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

from flask import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def basic():
    if request.method == 'POST':  # if method is post
        tower = request.form['tower']
        floor = request.form['floor']
        unit = request.form['unit']
        error = False
        li = [0, 0, 0, 0, 0, 0, 0]
        try:
            # get table value
            data = db.child("Demo").child(tower).child(floor).child("units").child(unit).child("unit_status").get()
            status = int(data.val())  # convert object file to int
            if status == 0:
                li[0] = 1
            else:
                li[status - 1] = 1
        except:
            error = True

        result = {
            "error": error,
            "categories": [
                "Yet to review",
                "Projectmanager Inspected & Snags given to Programhead",
                "Projectmanager Snags attended & Handed Over",
                "Customer Intimated for inspection",
                "Customer Snags Given to Architect",
                "Customer Snags Attended & Handed over to Supervisor",
                "Handed over to Customer"
            ],
            "data": li
        }
        return render_template("index.html", data=result)


    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
