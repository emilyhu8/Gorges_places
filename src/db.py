from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
  __tablename__="category"
  id=db.Column(db.Integer, primary_key=True, autoincrement=True)
  name=db.Column(db.String, nullable=False)
  places=db.relationship("Place", cascade="delete")
  
  def __init__ (self, **kwargs):
    self.name=kwargs.get("name", "")
  
  def serialize (self):
    return {
      "id": self.id, 
      "name": self.name,
      "places": [p.simple_serialize() for p in self.places],     
    }

  def simple_serialize(self):
    return {
      "id": self.id, 
      "name": self.name, 
    }

class Place (db.Model):
  __tablename__="place"
  id=db.Column(db.Integer, primary_key=True, autoincrement = True)
  name = db.Column(db.String, nullable = False)
  description = db.Column (db.String, nullable = False)
  category_id=db.Column(db.String, db.ForeignKey("category.id"))
  activities = db.relationship ("Activity", cascade="delete")
  ratings = db.relationship ("PlaceReview", cascade= "delete")

  def __init__ (self, **kwargs):
    """
    Creates a Place object
    """
    self.name = kwargs.get("name", "")
    self.description = kwargs.get ("description", "")
    self.category_id=kwargs.get("category_id", "")
  
  def serialize (self):
    """
    Serializes a Place object
    """
    return {
      "id": self.id, 
      "name": self.name, 
      "description": self.description, 
      "category": (Category.query.filter_by(id=self.category_id).first()).simple_serialize(),
      "activities": [a.simple_serialize() for a in self.activities], 
      "ratings": [r.simple_serialize() for r in self.ratings], 
    }
  
  def simple_serialize(self):
    """
    Simple serializes a Place object
    """
    return {
      "id": self.id,
      "name": self.name, 
      "description": self.description
    }

class Activity (db.Model):
  __tablename__="activity"
  id=db.Column(db.Integer, primary_key = True, autoincrement = True)
  name=db.Column(db.String, nullable=False)
  description=db.Column(db.String, nullable=False)
  completed = db.Column(db.Boolean, nullable =False)
  place_id = db.Column(db.Integer, db.ForeignKey("place.id"))

  def __init__ (self, **kwargs):
    """
    Creates an Activity object
    """
    self.name=kwargs.get("name", "")
    self.description=kwargs.get("description", "")
    self.completed=kwargs.get("completed", "")
    self.place_id=kwargs.get("place_id", "")

  def serialize(self):
    """
    Serialize an Activity object
    """
    return {
      "id": self.id, 
      "name": self.name, 
      "description": self.description,
      "complete": self.completed,
      "place": (Place.query.filter_by(id=self.place_id).first()).simple_serialize(), 
    }
  
  def simple_serialize(self):
    """
    Simple Serializes an Activity object
    """
    return {
      "id": self.id, 
      "name": self.name, 
      "description": self.description,
      "completed": self.completed
    }

class PlaceReview(db.Model):
  __tablename__="place_review"
  id=db.Column(db.Integer, primary_key =True, autoincrement = True)
  username=db.Column(db.String, nullable=False)
  rating = db.Column(db.Integer, nullable=False)
  place_id = db.Column(db.Integer, db.ForeignKey("place.id"))

  def __init__(self, **kwargs):
    """
    Creates a PlaceReview object
    """
    self.username=kwargs.get("username", "")
    self.rating=kwargs.get("rating", "")
    self.place_id=kwargs.get("place_id", "")

  def serialize(self):
    """
    Serializes a PlaceReview object
    """
    return {
      "id": self.id, 
      "username": self.username, 
      "rating": self.rating, 
    }
  
  def simple_serialize(self):
    """
    Simple Serializes a PlaceReview object
    """
    return {
      "username": self.username, 
      "rating": self.rating, 
    }





