from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Place (db.Model):
  __tablename__="place"
  id=db.Column(db.Integer, primary_key=True, autoincrement = True)
  name = db.Column(db.String, nullable = False)
  description = db.Column (db.String, nullable = False)
  activities = db.relationship ("Activity", cascade="delete")
  ratings = db.relationship ("Review", cascade= "delete")
  comments = db.relationship ("Review", cascade ="delete")

  def __init__ (self, **kwargs):
    """
    Creates a Place object
    """
    self.name = kwargs.get("name", "")
    self.description = kwargs.get ("description", "")
  
  def serialize (self):
    """
    Serializes a Place object
    """
    return {
      "id": self.id, 
      "name": self.name, 
      "description": self.description, 
      "activities": [a.simple_serialize() for a in self.activities], 
      "ratings": [r.simple_serialize() for r in self.ratings], 
      "comments": [c.simple_serialize() for c in self.comments] 
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
  place_id = db.Column(db.String, db.ForeignKey("place.id"), nullable=True)
  ratings = db.relationship ("Review", cascade= "delete")
  comments = db.relationship ("Review", cascade ="delete")

  def __init__ (self, **kwargs):
    """
    Creates an Activity object
    """
    self.name=kwargs.get("name", "")
    self.description=kwargs.get("description", "")

  def serialize(self):
    """
    Serialize an Activity object
    """
    return {
      "id": self.id, 
      "name": self.name, 
      "description": self.description, 
      "place": (Place.query.filter_by(id=self.place_id)).simple_serialize(), 
      "review": (Review.query.filter_by (id=self.review_id)).simple_serialize()
    }
  
  def simple_serialize(self):
    """
    Simple Serializes an Activity object
    """
    return {
      "id": self.id, 
      "name": self.name, 
      "description": self.description
    }

class Review(db.Model):
  __tablename__="review"
  id=db.Column(db.Integer, primary_key =True, autoincrement = True)
  username=db.Column(db.String, nullable=False)
  rating = db.Column(db.Integer, nullable=False)
  comment = db.Column(db.String, nullable= True)
  place_id = db.Column(db.String, db.ForeignKey("place.id"), nullable=True)
  activity_id = db.Column(db.String, db.ForeignKey("activity.id"), nullable=True)

  def __init__(self, **kwargs):
    """
    Creates a Review object
    """
    self.username=kwargs.get("username", "")
    self.rating=kwargs.get("rating", "")
    self.comment=kwargs.get("comment", "")

  def serialize(self):
    """
    Serializes a Review object
    """
    return {
      "id": self.id, 
      "username": self.username, 
      "rating": self.rating, 
      "comment": self.comment, 
      "place": (Place.query.filter_by_id(id=self.place_id).first()).simple_serialize(), 
      "activity": (Activity.query.filter_by_id(id=self.activity_id).first()).simple_serialize()
    }
  
  def simple_serialize(self):
    """
    Simple Serializes a User object
    """
    return {
      "username": self.username, 
      "rating": self.rating, 
      "comment": self.comment
    }




