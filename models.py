from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Appointment(db.Model):
    id = db.Column(db.String, primary_key=True)
    patient_name = db.Column(db.String)
    patient_phone = db.Column(db.String)
    doctor = db.Column(db.String)
    scheduled_for = db.Column(db.DateTime)
    status = db.Column(db.String, default='tentative')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Report(db.Model):
    id = db.Column(db.String, primary_key=True)
    appointment_id = db.Column(db.String, nullable=True)
    filename = db.Column(db.String)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String, default='processing')
    ocr_text = db.Column(db.Text)

class HumanTask(db.Model):
    id = db.Column(db.String, primary_key=True)
    appointment_id = db.Column(db.String, nullable=True)
    report_id = db.Column(db.String, nullable=True)
    task_type = db.Column(db.String)
    status = db.Column(db.String, default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
