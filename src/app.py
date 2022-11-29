from flask import Flask
import json
from flask import request
from db import db, Place, Activity
import os


app = Flask(__name__)
db_filename = "gp.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code

@app.route("/api/places/")
def get_places():
    """
    Endpoint for getting all places
    """
    places = [place.serialize() for place in Place.query.all()]
    return success_response({"places": places})

@app.route("/api/place/<int:place_id>/")
def get_place(place_id):
    """
    Endpoint for getting a place by id
    """
    place=Place.query.filter_by(id=place_id).first()
    if place is None:
        return failure_response("Place is not found")
    return success_response(place.serialize())

@app.route("/api/places/", methods=["POST"])
def create_place():
    """
    Endpoint for creating a new place
    """
    body=json.loads(request.data)
    if not body.get("name") or not body.get("description"):
        return failure_response("Please supply all fields.", 400)
    new_place = Place(name=body.get("name"), description=body.get("description"))
    db.session.add(new_place)
    db.session.commit()
    return success_response(new_place.serialize(), 201)

@app.route("/api/activities/")
def get_activities():
    """
    Endpoint for getting all activities
    """
    activities = [activity.serialize() for activity in Activity.query.all()]
    return success_response({"activities": activities})

@app.route("/api/places/<int:place_id>/activity/", methods=["POST"])
def create_activity(place_id):
    """
    Endpoint to create an activity to a place
    """
    place=Place.query.filter_by(id=place_id).first()
    body=json.loads(request.data)
    name=body.get("name")
    description=body.get("description")
    if name is None or description is None:
        return failure_response ("Please fill out all fields.", 400)
    new_activity=Activity(name=name, description=description, course_id=place_id)
    if place is None:
      new_activity=Activity(name=name, description=description)
    else:
      new_activity=Activity(name=name, description=description, place_id=place_id)
    db.session.add(new_activity)
    db.session.commit()
    return success_response (new_activity.serialize(), 201)



