from flask import Flask
import json
from flask import request
from db import db, Place, Activity, PlaceReview, Category
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

@app.route("/api/categories/")
def get_categories():
    """
    Endpoint for getting all categories
    """
    categories = [category.serialize() for category in Category.query.all()]
    return success_response({"categories": categories})

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
    Endpoint for getting a place by place id
    """
    place=Place.query.filter_by(id=place_id).first()
    if place is None:
        return failure_response("Place is not found")
    return success_response(place.serialize())

@app.route("/api/<int:category_id>/places/")
def get_places_by_category(category_id):
    """
    Endpoint for getting all places for a category
    """
    category=Category.query.filter_by(id=category_id).first()
    if category is None: 
        return failure_response ("Category can't be found")
    places = [place.serialize() for place in Place.query.filter_by(category_id=category_id)]
    return success_response({"places": places})

@app.route("/api/categories/", methods=["POST"])
def create_category():
    """
    Endpoint to create a category
    """
    body=json.loads(request.data)
    name=body.get("name")
    if name is None:
        return failure_response ("Please fill out all fields.", 400)
    new_category=Category(name=name)
    db.session.add(new_category)
    db.session.commit()
    return success_response (new_category.serialize(), 201)

@app.route("/api/<int:category_id>/place/", methods=["POST"])
def create_place(category_id):
    """
    Endpoint to create a place
    """
    category=Category.query.filter_by(id=category_id).first()
    if category is None: 
        return failure_response ("Category can't be found")
    body=json.loads(request.data)
    name=body.get("name")
    description=body.get("description")
    if name is None or description is None:
        return failure_response ("Please fill out all fields.", 400)
    new_place=Place(name=name, description=description, category_id=category_id)
    db.session.add(new_place)
    db.session.commit()
    return success_response (new_place.serialize(), 201)

@app.route("/api/<int:place_id>/activity/")
def get_activities(place_id):
    """
    Endpoint for getting all activities for a place
    """
    place=Place.query.filter_by(id=place_id).first()
    if place is None: 
        return failure_response ("Place can't be found")
    activities = [activity.serialize() for activity in Activity.query.filter_by(place_id=place_id)]
    return success_response({"activities": activities})

@app.route("/api/places/<int:place_id>/activity/", methods=["POST"])
def create_activity(place_id):
    """
    Endpoint to create an activity to a place
    """
    place=Place.query.filter_by(id=place_id).first()
    if place is None: 
        return failure_response ("Place can't be found")
    body=json.loads(request.data)
    name=body.get("name")
    description=body.get("description")
    completed=body.get("completed", False)
    if name is None or description is None:
        return failure_response ("Please fill out all fields.", 400)
    new_activity=Activity(name=name, description=description, completed= completed, place_id=place_id)
    db.session.add(new_activity)
    db.session.commit()
    return success_response (new_activity.serialize(), 201)

@app.route("/api/activity/<int:activity_id>/", methods=["DELETE"])
def delete_activity(activity_id):
    """
    Endpoint for deleting a specific activity by id
    """
    activity=Activity.query.filter_by(id=activity_id).first()
    if activity is None:
        return failure_response("Activity is not found")
    db.session.delete(activity)
    db.session.commit()
    return success_response(activity.serialize())

@app.route("/api/places/<int:place_id>/review/")
def get_reviews(place_id):
    """
    Endpoint to get reviews for a specific place
    """
    place=Place.query.filter_by(id=place_id).first()
    if place is None:
        return failure_response ("Place can't be found")
    reviews = [review.serialize() for review in PlaceReview.query.filter_by(place_id=place_id)]
    return success_response({"reviews": reviews})
    
@app.route("/api/places/<int:place_id>/review/", methods=["POST"])
def create_review(place_id):
    """
    Endpoint to create a review to a place
    """
    place=Place.query.filter_by(id=place_id).first()
    if place is None: 
        return failure_response ("Place can't be found")
    body=json.loads(request.data)
    username=body.get("username")
    rating=body.get("rating")
    if username is None or rating is None:
        return failure_response ("Please fill out all fields.", 400)
    new_review=PlaceReview(username=username,rating=rating, place_id=place_id)
    db.session.add(new_review)
    db.session.commit()
    return success_response (new_review.serialize(), 201)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8008, debug=True)



