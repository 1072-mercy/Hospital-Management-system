from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime




class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    EMail = db.Column(db.String(255), nullable=False, unique=True, index=True)# Add index here
    IDNumber = db.Column(db.String(255), nullable=False)
    Age = db.Column(db.String(255), nullable=False)
    DOB = db.Column(db.String(255), nullable=False)
    Gender = db.Column(db.String(10), nullable=False)
    Photo = db.Column(db.LargeBinary(length=(2**32)-1), nullable=False)
    Password = db.Column(db.String(255), nullable=False)

    Symptoms = db.Column(db.String(255), nullable=True)
    Sickness = db.Column(db.String(255), nullable=True)
    Medication = db.Column(db.String(255), nullable=True)


class T2(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    lno = db.Column(db.Integer, unique=True, nullable=False)
    idno = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    dob = db.Column(db.Date, unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phoneno = db.Column(db.Integer, unique=True, nullable=False)
    hospital = db.Column(db.String(50), nullable=False)
    specialization = db.Column(db.String(50), nullable=False)

    image_data = db.Column(db.LargeBinary, nullable=True)
    password = db.Column(db.String(128), nullable=False)


class PatientHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_email = db.Column(db.String(255), db.ForeignKey('patient.EMail'), nullable=False)
    Symptoms = db.Column(db.String(255), nullable=True)
    Sickness = db.Column(db.String(255), nullable=True)
    Medication = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    doctor_email = db.Column(db.String(255), nullable=False)  



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # ForeignKey referencing the 'EMail' column in 'Patient'
    patient_email = db.Column(db.String(255), db.ForeignKey('patient.EMail'), nullable=False)
    
    # Relationship attribute for easy access to associated comments
    patient = db.relationship('Patient', backref=db.backref('comments', lazy=True))



class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.String(20), nullable=False)
    before_eating = db.Column(db.Integer, nullable=False)
    after_eating = db.Column(db.Integer, nullable=False)
    bedtime = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(200), nullable=False)

    # Foreign key to relate with Patient
    patient_email = db.Column(db.String(255), db.ForeignKey('patient.EMail'), nullable=False)
    
    # Relationship with Patient
    patient = db.relationship('Patient',  backref=db.backref('diary', lazy=True))

# Foreign key to relate with Patient

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    hospital = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(5), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)
    comment = db.Column(db.String(255)) 


class DiabeticPatient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)


class DoctorsRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(100), nullable=False)
    doctor_hospital = db.Column(db.String(100), nullable=False)
    doctor_specialization = db.Column(db.String(50), nullable=False)
    doctor_email = db.Column(db.String(120), nullable=False)
    patient_email = db.Column(db.String(120), nullable=False)
    appointment_date = db.Column(db.String(10), nullable=False)
    comment = db.Column(db.String(255), nullable=True) 