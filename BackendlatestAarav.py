from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='./')

# Sample data
hospitals = [
    {"name": "Fortis Hospital", "specialties": "Cardiology, Neurology, Cosmetic Surgery", "location": "Gurugram"},
    {"name": "Safdarjung Hospital", "specialties": "Orthopedics, Oncology, Gastroenterology", "location": "Delhi"},
]

doctors = [
    {"name": "Dr. Ajit Kumar", "specialty": "Cardiology", "experience": "15 years"},
    {"name": "Dr. Vanaj Mathur", "specialty": "Cosmetic Surgery", "experience": "10 years"},
]

treatments = [
    {"name": "Heart Surgery", "cost": "$5,000 - $10,000", "top_hospitals": "Safdarjung, Fortis"},
    {"name": "Cosmetic Surgery", "cost": "$3,000 - $8,000", "top_hospitals": "AIMS, Safdarjung"},
]

@app.route('/')
def home():
    return render_template('Vanshri.html', hospitals=hospitals, doctors=doctors, treatments=treatments)

@app.route('/redirect', methods=['POST'])
def handle_redirect():
    user_input = request.form.get('query', '').lower()
    
    # Check user input and redirect accordingly
    if "fortis" in user_input:
        return redirect(url_for('hospital_details', hospital_name="Fortis Hospital"))
    elif "ajit" in user_input or "cardiology" in user_input:
        return redirect(url_for('doctor_details', doctor_name="Dr. Ajit Kumar"))
    elif "heart" in user_input or "surgery" in user_input:
        return redirect(url_for('treatment_details', treatment_name="Heart Surgery"))
    else:
        # Redirect to a generic search results page
        return redirect(url_for('search', q=user_input))

@app.route('/hospital/<hospital_name>')
def hospital_details(hospital_name):
    # Example for hospital details
    hospital = next((h for h in hospitals if h['name'] == hospital_name), None)
    if hospital:
        return render_template('hospital_details.html', hospital=hospital)
    return "Hospital not found", 404

@app.route('/doctor/<doctor_name>')
def doctor_details(doctor_name):
    # Example for doctor details
    doctor = next((d for d in doctors if d['name'] == doctor_name), None)
    if doctor:
        return render_template('doctor_details.html', doctor=doctor)
    return "Doctor not found", 404

@app.route('/treatment/<treatment_name>')
def treatment_details(treatment_name):
    # Example for treatment details
    treatment = next((t for t in treatments if t['name'] == treatment_name), None)
    if treatment:
        return render_template('treatment_details.html', treatment=treatment)
    return "Treatment not found", 404

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    # Implement search functionality (like the previous example)
    return render_template('Vanshri.html', query=query)

if __name__ == '__main__':
    app.run(debug=True)
