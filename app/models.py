from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ChatMessage(db.Model):
    id = db.Sring(db.Integer, primary_key=True)
    message_text = db.String(db.Text, nullable=False)
    timestamp = db.String(db.DateTime, default=datetime.utcnow, nullable=False)
    is_user = db.String(db.Boolean, default=True, nullable=False)
    conversation_id = db.String(db.String(36), db.ForeignKey('conversation.id'))