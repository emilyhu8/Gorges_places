from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

place_association_table= db.Table(
  "place_association_table",
  db.Column("category_id", db.Integer, db.ForeignKey("category.id")),
  db.Column("activity_id", db.Integer, db.ForeignKey("place.id")) 
)

activity_association_table= db.Table(
  "activity_association_table",
  db.Column("category_id", db.Integer, db.ForeignKey("category.id")),
  db.Column("activity_id", db.Integer, db.ForeignKey("activity.id")) 
)

class Place (db.Model):
  __tablename__="place"
  id=db.Column(db.Integer, primary_key=True, autoincrement = True)
  name = db.Column(db.String, nullable = False)
  description = db.Column (db.String, nullable = False)
  category=db.relationship("Category", secondary = place_association_table, back_populates=True)
  activities = db.relationship ("Activity", cascade="delete")
  ratings = db.relationship ("PlaceReview", cascade= "delete")
  comments = db.relationship ("PlaceReview", cascade ="delete")

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
      "category": [c.simple_serialize() for c in self.category],
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
  category=db.relationship("Category", secondary = activity_association_table, back_populates=True)
  completed = db.Column(db.Boolean, nullable =True)
  place_id = db.Column(db.String, db.ForeignKey("place.id"), nullable=True)
  ratings = db.relationship ("ActivityReview", cascade= "delete")
  comments = db.relationship ("ActivityReview", cascade ="delete")

  def __init__ (self, **kwargs):
    """
    Creates an Activity object
    """
    self.name=kwargs.get("name", "")
    self.description=kwargs.get("description", "")
    self.completed=kwargs.get("completed", False)

  def serialize(self):
    """
    Serialize an Activity object
    """
    return {
      "id": self.id, 
      "name": self.name, 
      "description": self.description,
      "category": [c.simple_serialize() for c in self.category], 
      "complete": self.completed,
      "place": (Place.query.filter_by(id=self.place_id)).simple_serialize(), 
      "ratings": [r.simple_serialize() for r in self.ratings], 
      "comments": [c.simple_serialize() for c in self.comments] 
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
  comment = db.Column(db.String, nullable= True)
  place_id = db.Column(db.String, db.ForeignKey("place.id"), nullable=True)

  def __init__(self, **kwargs):
    """
    Creates a PlaceReview object
    """
    self.username=kwargs.get("username", "")
    self.rating=kwargs.get("rating", "")
    self.comment=kwargs.get("comment", "")

  def serialize(self):
    """
    Serializes a PlaceReview object
    """
    return {
      "id": self.id, 
      "username": self.username, 
      "rating": self.rating, 
      "comment": self.comment, 
      "place": (Place.query.filter_by_id(id=self.place_id).first()).simple_serialize(), 
    }
  
  def simple_serialize(self):
    """
    Simple Serializes a PlaceReview object
    """
    return {
      "username": self.username, 
      "rating": self.rating, 
      "comment": self.comment
    }

class ActivityReview(db.Model):
  __tablename__="activity_review"
  id=db.Column(db.Integer, primary_key =True, autoincrement = True)
  username=db.Column(db.String, nullable=False)
  rating = db.Column(db.Integer, nullable=False)
  comment = db.Column(db.String, nullable= True)
  activity_id = db.Column(db.String, db.ForeignKey("activity.id"), nullable=True)

  def __init__(self, **kwargs):
    """
    Creates a ActivityReview object
    """
    self.username=kwargs.get("username", "")
    self.rating=kwargs.get("rating", "")
    self.comment=kwargs.get("comment", "")

  def serialize(self):
    """
    Serializes a ActivityReview object
    """
    return {
      "id": self.id, 
      "username": self.username, 
      "rating": self.rating, 
      "comment": self.comment, 
      "activity": (Activity.query.filter_by_id(id=self.activity_id).first()).simple_serialize()
    }
  
  def simple_serialize(self):
    """
    Simple Serializes a ActivityReview object
    """
    return {
      "username": self.username, 
      "rating": self.rating, 
      "comment": self.comment
    }

class Category(db.Model):
  __tablename__="category"
  id=db.Column(db.Integer, primary_key=True, autoincrement=True)
  name=db.Column(db.String, nullable=False)
  activities=db.relationship("Activity", secondary=activity_association_table, back_populates=True)
  activities=db.relationship("Place", secondary=place_association_table, back_populates=True)

  def __init__ (self, **kwargs):
    self.name=kwargs.get("name", "")
  
  def serialize (self):
    return {
      "id": self.id, 
      "name": self.name,
      "places": [p.serialize() for p in self.places],
      "activities": [a.serialize() for a in self.activities]     
    }

  def simple_serlialize(self):
    return {
      "id": self.id, 
      "name": self.name, 
    }





