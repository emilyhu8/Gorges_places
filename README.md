# Gorges_places

This is the backend repo for the Gorges Places app.

We have 12 routes, all listed in the API specification. 

We have three database models: Category, Place, Activity, PlaceReview, and PlaceReview.

- Category:
  __tablename__="category"
  id=db.Column(db.Integer, primary_key=True, autoincrement=True)
  name=db.Column(db.String, nullable=False)
  places=db.relationship("Place", cascade="delete")
  
- Place
  __tablename__="place"
  id=db.Column(db.Integer, primary_key=True, autoincrement = True)
  name = db.Column(db.String, nullable = False)
  description = db.Column (db.String, nullable = False)
  category_id=db.Column(db.String, db.ForeignKey("category.id"))
  activities = db.relationship ("Activity", cascade="delete")
  ratings = db.relationship ("PlaceReview", cascade= "delete")
  
 - Activity
  __tablename__="activity"
  id=db.Column(db.Integer, primary_key = True, autoincrement = True)
  name=db.Column(db.String, nullable=False)
  description=db.Column(db.String, nullable=False)
  completed = db.Column(db.Boolean, nullable =False)
  place_id = db.Column(db.Integer, db.ForeignKey("place.id"))
 
 - PlaceReview
   __tablename__="place_review"
  id=db.Column(db.Integer, primary_key =True, autoincrement = True)
  username=db.Column(db.String, nullable=False)
  rating = db.Column(db.Integer, nullable=False)
  place_id = db.Column(db.Integer, db.ForeignKey("place.id"))

- PlaceSimple
  __tablename__="place_simple"
  id=db.Column(db.Integer, primary_key=True, autoincrement = True)
  name = db.Column(db.String, nullable = False)
  description = db.Column (db.String, nullable = False)
  category=db.Column(db.String, nullable=False)
  activity = db.Column (db.String, nullable=True)
