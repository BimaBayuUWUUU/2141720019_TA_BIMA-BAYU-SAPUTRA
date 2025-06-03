# models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class InputData(db.Model):
    __tablename__ = 'input_data'
    id = db.Column(db.Integer, primary_key=True)
    r = db.Column(db.Float)
    g = db.Column(db.Float) 
    b = db.Column(db.Float)  
    file_path = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class ClassificationResult(db.Model):
    __tablename__ = 'classification_results'
    id = db.Column(db.Integer, primary_key=True)
    input_data_id = db.Column(db.Integer, db.ForeignKey('input_data.id'))
    model_name = db.Column(db.String(50))
    predicted_class = db.Column(db.String(20))
    classified_at = db.Column(db.DateTime, default=datetime.utcnow)

    input_data = db.relationship("InputData", backref="results")
    
class ClassificationResultFile(db.Model):
    __tablename__ = 'classification_result_file'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    input_file_id = db.Column(db.Integer, db.ForeignKey('input_data.id'))