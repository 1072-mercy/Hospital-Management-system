from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session

from io import BytesIO

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session


from patients.patient import patient
from mydata import Patient,Comment,Appointment,PatientHistory,T2,DiabeticPatient,Diary,DoctorsRequest,db
from sqlalchemy import Index
from datetime import datetime 






app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://team:0987654321@localhost/start'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

db.init_app(app)





with app.app_context():
    db.create_all()


app.register_blueprint(patient, url_prefix="/HIMS/")




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        lno = request.form['lno']
        idno = request.form['idno']
        name = request.form['name']
        dob = request.form['dob']
        email = request.form['email']
        phoneno = request.form['phoneno']
        hospital = request.form['hospital']
        specialization = request.form['specialization']
        password = request.form['password']

        existing_entry = T2.query.filter_by(idno=idno).first()

        if existing_entry:
            flash('Person already exists. Choose a different name.', 'danger')
            return redirect(url_for('register'))

        if 'photo' in request.files:
            photo_data = request.files['photo'].read()
        else:
            photo_data = None

        new_entry = T2(lno=lno, idno=idno, name=name, dob=dob, email=email, phoneno=phoneno, hospital=hospital, specialization=specialization, image_data=photo_data, password=password)
        db.session.add(new_entry)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        
        entered_password = request.form['password']  # Use a different variable name

        user = T2.query.filter_by(email=email).first()

        if user and user.password == entered_password:
            # Store the user's ID in the session
            session['user_id'] = user.id
            session['user_email'] = user.email
            
            
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please check your email or password.', 'danger')

    return render_template('drlogin.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    user_id = session.get('user_id')
    
    # Check if user is logged in
    if user_id is None:
        flash('Please log in first.', 'danger')
        return redirect(url_for('login'))

    # Query and display information for the logged-in user only
    user_data = T2.query.filter_by(id=user_id).first()
    return render_template('doctor1.html', try_data=[user_data])


@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    # Retrieve data from the Appointment table
    appointments = Appointment.query.all()

    # Pass the appointments data to the template
    return render_template('appointmentsd.html', appointments=appointments)





@app.route('/records/<email>', methods=['GET', 'POST'])
def records(email):
    # Fetch details for the given email from the Patient table
    patient_details = Patient.query.filter_by(EMail=email).first()

    # Fetch history entries for the given email from the PatientHistory table
    history_entries = PatientHistory.query.filter_by(patient_email=email).all()

    # Pass both patient details and history entries to the records template
    return render_template('records.html', patient_details=patient_details, history_entries=history_entries)
@app.route('/update_records/<email>', methods=['GET', 'POST'])
def update_records(email):
    # Fetch patient details for the given email
    patient = Patient.query.filter_by(EMail=email).first()

    if request.method == 'POST':
        # Create a new entry in PatientHistory
        doctor_email = session.get('user_email')
        history_entry = PatientHistory(
            patient_email=patient.EMail,
            doctor_email=doctor_email, 

            Symptoms=request.form.get('symptoms'),
            Sickness=request.form.get('sickness'),
            Medication=request.form.get('medication'),
            timestamp=datetime.utcnow()  # Add timestamp for tracking when the entry was created
        )

        # Commit the changes to the database
        db.session.add(history_entry)
        db.session.commit()

        # Redirect to the records page or another appropriate page
        return redirect(url_for('records', email=email))

    # Fetch all history entries for the given patient
    history_entries = PatientHistory.query.filter_by(patient_email=patient.EMail).all()

    # Return a response in case the request method is not 'POST'
    return render_template('updaterecords.html', patient=patient, history_entries=history_entries)

@app.route('/doctor_appointment',methods=['GET', 'POST'])
def doctor_appointment():
    if request.method == 'POST':
        # Fetch the doctor information based on the user's session
        doctor = T2.query.filter_by(email=session['user_email']).first()

        # Get data from the form submission
        doctor_name = doctor.name
        doctor_hospital = doctor.hospital
        doctor_specialization = doctor.specialization
        doctor_email = doctor.email
        patient_email = request.form.get('patient_email')
        appointment_date = request.form.get('appointment_date')
        comment = request.form.get('comment')

        # Create a new DoctorsRequest object and add it to the database
        new_request = DoctorsRequest(
            doctor_name=doctor_name,
            doctor_hospital=doctor_hospital,
            doctor_specialization=doctor_specialization,
            doctor_email=doctor_email,
            patient_email=patient_email,
            appointment_date=appointment_date,
            comment=comment
        )

        # Add the new request to the database
        db.session.add(new_request)
        db.session.commit()

        # Redirect to a success page or another appropriate route
        return redirect(url_for('show_diabetic'))

    # Handle cases where the request method is not POST
    return render_template('patients.html') 





@app.route('/patients', methods=['GET', 'POST'])
def patients():

    return render_template('patients.html')

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')

        # Create a new diabetic patient
        new_patient = DiabeticPatient(name=name, email=email)

        # Add the patient to the database
        db.session.add(new_patient)
        db.session.commit()

        # Redirect to the main patients page
        return redirect(url_for('patients'))

    # If it's a GET request, render the template for adding patients
    return render_template('enterp.html')


@app.route('/show_diabetic')
def show_diabetic():
    diabetic_patients = DiabeticPatient.query.all()
   
    return render_template('patients.html', diabetic_patients=diabetic_patients)

@app.route('/personaldiary/<string:patient_email>')
def personaldiary(patient_email):
    # Fetch the patient based on the provided email
    patient = Patient.query.filter_by(EMail=patient_email).first()

    if patient:
        # Fetch diary entries for the specific patient
        diary_entries = Diary.query.filter_by(patient_email=patient_email).all()
        return render_template('show.html', patient=patient, diary_entries=diary_entries)
    else:
        return render_template('error.html', message='Patient not found')



@app.route('/approvals', methods=['GET', 'POST'])
def approvals():

    return render_template('approvals.html')

@app.route('/billing')
def billing():
    return render_template('approvals.html')
@app.route('/show_diary')
def show_diary():
    # Fetch data from the "Diary" table
    diary_entries = Diary.query.all()

    return render_template('diary2.html', diary_entries=diary_entries)

@app.route('/useemail/<int:patient_email>')
def useemail(patient_email):
    useemail
    return render_template('patients.html',patient_email=patient_email)





@app.route('/display_image/<int:entry_id>')
def display_image(entry_id):
    entry = T2.query.get(entry_id)
    return send_file(BytesIO(entry.image_data), mimetype='image/jpeg')

if __name__ == "__main__":
    app.register_blueprint(patient, url_prefix="/HIMS/")
    app.run(debug=True)