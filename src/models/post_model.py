from src import db
from datetime import datetime


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    slug = db.Column(db.String(255))
