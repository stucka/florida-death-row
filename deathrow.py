from flask import Flask, render_template, redirect, url_for     # pip install -r requirements.txt
from roster import ROSTER
from nameparser import HumanName
import datetime

app = Flask(__name__)
#app.config['SECRET_KEY'] = '14uff!eumps&w00ze!s'
application = app
#get all of the IDs and names and append them to the list names
today = datetime.datetime.today()

def ap_string(mdy):
    text = datetime.datetime.strptime(mdy, "%m/%d/%y").strftime("%B %d, %Y")  # Take string formated as m/d/y, return as "January 05, 2017"
    replacementpairs = [
        ("January 0", "Jan. "), ("February 0", "Feb. "), ("August 0", "Aug. "), ("September 0", "Sept. "), ("October 0", "Oct. "), ("November 0", "Nov. "), ("December 0", "Dec. "),
        ("March 0", "March "), ("April 0", "April "), ("May 0", "May "), ("June 0", "June "), ("July 0", "July "),
        ("January ", "Jan. "), ("February ", "Feb. "), ("August ", "Aug. "), ("September ", "Sept. "), ("October ", "Oct. "), ("November ", "Nov. "), ("December ", "Dec. ")
    ]
    for pair in replacementpairs:
        source, destination = pair
        text = text.replace(source, destination)
    return(text)


def get_names(source):
    names = []
    for row in source:
        id = row["id"]
        name = row["name"]
        photo = row["photo"]
        names.append([id, name])
    return names, photo

# get the information for each ID
def get_inmatedata(source, id):
    for row in source:
        if id == str( row["id"] ):
            # decode handles accented characters
            name = row["name"]
            cleanname = HumanName(name)
            cleanname.capitalize()
            # print(parsedname)
            race = row["race"]
            race = race[0] + race[1:].lower()
            photo = row["photo"] 
            sex = row["sex"].lower()
            dob = row["dob"]
            age =  datetime.datetime.strptime(dob, "%m/%d/%y")
            age = today - age
            age = str(int(age.days/365.25)) # Round down years, store as text
            print(age)
#             age = str(round(age.days/365.25))   # Round age to number of years
            dob = ap_string(dob)
            entry = row["entry"]
            facility = row["facility"]
            custody = row["custody"]
    return id, cleanname, race, photo, sex, dob, entry, facility, custody, age

#set the homepage and the /restaurants.html to run the function to get information using the python dictionary INSPECTIONS
@app.route('/')
@app.route('/inmates.html')
def inmates():
    names, photo = get_names(ROSTER)
    return render_template('inmates.html', pairs=names, photo=photo)



#make a path for the /restaurant with each restaurant id and show the information for each restaurant with each ID
@app.route('/inmate/<id>.html')
def inmate(id):
    id, name, race, photo, sex, dob, entry, facility, custody, age = get_inmatedata(ROSTER, id)
    return render_template('inmate.html', pairs=name, name=name, race=race, photo=photo, sex=sex, dob=dob, entry=entry, facility=facility, custody=custody, age=age)

if __name__ == '__main__':
    app.run(debug=True)
