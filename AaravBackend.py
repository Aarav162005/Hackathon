from flask import Flask, render_template, request
app = Flask(__name__, template_folder='./')

# Sample data (usually stored in a database)
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

# Home route
@app.route('/')
def home():
    return render_template('Anvi.html', hospitals=hospitals, doctors=doctors, treatments=treatments)

# Search route
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    # Simple search functionality: check if the query matches any hospital, doctor, or treatment
    search_results = {
        'hospitals': [hospital for hospital in hospitals if query.lower() in hospital['name'].lower() or query.lower() in hospital['specialties'].lower()],
        'doctors': [doctor for doctor in doctors if query.lower() in doctor['name'].lower() or query.lower() in doctor['specialty'].lower()],
        'treatments': [treatment for treatment in treatments if query.lower() in treatment['name'].lower()],
    }
    
   
    
    return render_template('Anvi.html', hospitals=search_results['hospitals'], doctors=search_results['doctors'], treatments=search_results['treatments'],)

if __name__ == '__main__':
    app.run(debug=True)
