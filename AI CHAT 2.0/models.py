from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  # ← ADD THIS LINE

db = SQLAlchemy()

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_msg = db.Column(db.Text)
    bot_reply = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)