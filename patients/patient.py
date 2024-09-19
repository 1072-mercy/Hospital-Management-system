from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from mydata import Patient, Appointment, Comment,Diary,PatientHistory,T2,DoctorsRequest, db


patient = Blueprint("patient", __name__, static_folder="static", template_folder="templates")

@patient.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['Name']
        email = request.form['EMail']
        password = request.form['Password']
        idno = request.form['IDNumber']
        age = request.form['age']
        dob = request.form['date']
        gender = request.form['gender']

        existing_entry = Patient.query.filter_by(IDNumber=idno).first()

        if existing_entry:
            flash('Person already exists. Choose a different name.', 'danger')
            return redirect(url_for('patient.register'))

        if 'photo' in request.files:
            photo_data = request.files['photo'].read()
        else:
            photo_data = None

        new_entry = Patient(
            Name=name,
            EMail=email,
            IDNumber=idno,
            Age=age,
            DOB=dob,
            Gender=gender,
            Photo=photo_data,
            Password=password
        )

        db.session.add(new_entry)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('patient.login'))

    return render_template('register2.html')


@patient.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        entered_password = request.form['password']

        user = Patient.query.filter_by(EMail=email).first()

        if user and user.Password == entered_password:
            # Store the user's ID in the session
            session['user_id'] = user.id
            session['user_email'] = user.EMail

           
            return redirect(url_for('patient.home'))
        else:
            flash('Login failed. Please check your email or password.', 'danger')

    return render_template('plogin1.html')

@patient.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('patient.home'))
    user_id = session.get('user_id')
    
    # Check if user is logged in
    if user_id is None:
        flash('Please log in first.', 'danger')
        return redirect(url_for('login'))

    user_data = Patient.query.filter_by(id=user_id).first()
    return render_template('pdash.html', try_data=[user_data])

@patient.route('/d')
def display_image():
    # Assuming your image is named "mercy.jpg" in the "images" folder
    return render_template('plogin1.html')



@patient.route('/medication')
 # Assuming you are using login_required decorator
def medication():
    
    # Fetch all medication entries connected to the email of the logged-in user
    medication_entries = (
        db.session.query(
            T2.name,
            T2.email.label('doctor_email'),
            PatientHistory.Medication,
            PatientHistory.timestamp
        )
        .join(PatientHistory, T2.email == PatientHistory.doctor_email)
        .filter(PatientHistory.patient_email == session.get('user_email'))  # Filter by the email of the logged-in user
        .all()
    )

    return render_template('medication1.html', medication_entries=medication_entries)



@patient.route('/comments', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        text = request.form.get('comment_text')

        # Retrieve the email from the session
        patient_email = session.get('user_email')

        # Validate that text is not None or empty
        if text is None or text.strip() == '':
            return 'Text cannot be empty', 400

        # Ensure that patient_email is not None before creating the comment
        if patient_email is not None:
            # Create a new comment instance
            new_comment = Comment(text=text, patient_email=patient_email)

            # Add the comment to the database session
            db.session.add(new_comment)

            # Commit the changes to the database
            db.session.commit()

            return 'Comment added successfully'
        else:
            return 'User not logged in', 400

    return render_template('comment2.html')


# Flask route
@patient.route('/diary', methods=['GET', 'POST'])
def diary():

    if request.method == 'POST':
        day_of_week = request.form.get('dayOfWeek')
        before_eating = request.form.get('beforeEating')
        after_eating = request.form.get('afterEating')
        bedtime = request.form.get('bedtime')
        comment = request.form.get('comment')
        patient_email = session.get('user_email')

        entry = Diary(
            day_of_week=day_of_week,
            before_eating=before_eating,
            after_eating=after_eating,
            bedtime=bedtime,
            comment=comment,
            patient_email=patient_email
        )

       

        db.session.add(entry)
        db.session.commit()
        
        return render_template('diary.html')
        

    return render_template('diary.html')



@patient.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'POST':
        # Retrieve form data using request.form.get
        name = request.form.get('name')
        hospital = request.form.get('hospital')
        specialization = request.form.get('specialization')
        phone = request.form.get('phone')
        email = request.form.get('email')
        area = request.form.get('area')
        city = request.form.get('city')
        time = request.form.get('time')  # Retrieve time from hidden input
        date = request.form.get('date')  # Retrieve date from hidden input
        postcode = request.form.get('postcode')

        # Create an Appointment object and add it to the database
        appointment = Appointment(
            name=name, hospital=hospital, specialization=specialization,
            phone=phone, email=email, area=area, city=city, time=time, date=date, postcode=postcode
        )
        db.session.add(appointment)
        db.session.commit()
        return "Appointment booked successfully!"

    return render_template('appointments.html')

@patient.route('/billing')
def billing():
    return render_template('billing.html')


