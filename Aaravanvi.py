from flask import Flask, render_template, request, jsonify
from datetime import datetime
import re

app = Flask(__name__, template_folder='./')

# Enhanced sample data with more fields and structure
hospitals = [
    {
        "id": 1,
        "name": "Fortis Hospital",
        "specialties": ["Cardiology", "Neurology", "Cosmetic Surgery"],
        "location": "Gurugram",
        "rating": 4.5,
        "emergency_contact": "+91-124-4921021",
        "facilities": ["24/7 Emergency", "ICU", "Blood Bank", "Pharmacy"],
        "insurance_accepted": ["MaxBupa", "ICICI Lombard", "Star Health"]
    },
    {
        "id": 2,
        "name": "Safdarjung Hospital",
        "specialties": ["Orthopedics", "Oncology", "Gastroenterology"],
        "location": "Delhi",
        "rating": 4.2,
        "emergency_contact": "+91-011-26707444",
        "facilities": ["24/7 Emergency", "Blood Bank", "Diagnostic Center"],
        "insurance_accepted": ["Government Health Scheme", "CGHS", "ECHS"]
    },
]

doctors = [
    {
        "id": 1,
        "name": "Dr. Ajit Kumar",
        "specialty": "Cardiology",
        "experience": "15 years",
        "qualifications": ["MBBS", "MD", "DM Cardiology"],
        "available_days": ["Monday", "Wednesday", "Friday"],
        "consultation_hours": "9:00 AM - 5:00 PM",
        "hospital_id": 1
    },
    {
        "id": 2,
        "name": "Dr. Vanaj Mathur",
        "specialty": "Cosmetic Surgery",
        "experience": "10 years",
        "qualifications": ["MBBS", "MS", "MCh Plastic Surgery"],
        "available_days": ["Tuesday", "Thursday", "Saturday"],
        "consultation_hours": "10:00 AM - 6:00 PM",
        "hospital_id": 1
    },
]

treatments = [
    {
        "id": 1,
        "name": "Heart Surgery",
        "cost": "$5,000 - $10,000",
        "top_hospitals": ["Safdarjung", "Fortis"],
        "duration": "4-6 hours",
        "recovery_time": "4-6 weeks",
        "success_rate": "95%",
        "prerequisites": ["ECG", "Blood Tests", "Chest X-ray"]
    },
    {
        "id": 2,
        "name": "Cosmetic Surgery",
        "cost": "$3,000 - $8,000",
        "top_hospitals": ["AIMS", "Safdarjung"],
        "duration": "2-4 hours",
        "recovery_time": "2-3 weeks",
        "success_rate": "98%",
        "prerequisites": ["Medical History", "Physical Examination"]
    },
]

def search_data(query, data, fields):
    """
    Advanced search function that checks multiple fields and returns relevance scores
    """
    results = []
    query = query.lower()
    query_terms = query.split()
    
    for item in data:
        score = 0
        matches = set()
        
        for field in fields:
            field_value = item.get(field, '')
            if isinstance(field_value, list):
                field_value = ' '.join(map(str, field_value))
            field_value = str(field_value).lower()
            
            # Check for exact matches
            if query in field_value:
                score += 3
                matches.add(field)
            
            # Check for partial matches
            for term in query_terms:
                if term in field_value:
                    score += 1
                    matches.add(field)
        
        if score > 0:
            results.append({
                'item': item,
                'score': score,
                'matched_fields': list(matches)
            })
    
    # Sort results by score in descending order
    results.sort(key=lambda x: x['score'], reverse=True)
    return [r['item'] for r in results]

@app.route('/')
def home():
    """Home route with all data"""
    return render_template('Hack2.html', 
                         hospitals=hospitals, 
                         doctors=doctors, 
                         treatments=treatments,
                         current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/search', methods=['GET'])
def search():
    """Enhanced search route with advanced filtering"""
    query = request.args.get('q', '').strip()
    category = request.args.get('category', 'all')
    
    if not query:
        return home()
    
    search_results = {
        'hospitals': search_data(query, hospitals, ['name', 'specialties', 'location', 'facilities']),
        'doctors': search_data(query, doctors, ['name', 'specialty', 'qualifications', 'available_days']),
        'treatments': search_data(query, treatments, ['name', 'top_hospitals', 'prerequisites'])
    }
    
    # Filter by category if specified
    if category != 'all':
        for key in search_results:
            if key != category:
                search_results[key] = []
    
    return render_template('Aaravanvi.html',
                         hospitals=search_results['hospitals'],
                         doctors=search_results['doctors'],
                         treatments=search_results['treatments'],
                         search_query=query,
                         current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/api/search', methods=['GET'])
def api_search():
    """API endpoint for search functionality"""
    query = request.args.get('q', '').strip()
    category = request.args.get('category', 'all')
    
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    search_results = {
        'hospitals': search_data(query, hospitals, ['name', 'specialties', 'location', 'facilities']),
        'doctors': search_data(query, doctors, ['name', 'specialty', 'qualifications', 'available_days']),
        'treatments': search_data(query, treatments, ['name', 'top_hospitals', 'prerequisites'])
    }
    
    if category != 'all':
        return jsonify({category: search_results.get(category, [])}), 200
    
    return jsonify(search_results), 200

@app.route('/hospital/<int:hospital_id>')
def hospital_details(Aaravanvi.html):
    """Route to get detailed information about a specific hospital"""
    hospital = next((h for h in hospitals if h['id'] == hospital_id), None)
    if hospital:
        # Get doctors working at this hospital
        hospital_doctors = [d for d in doctors if d['hospital_id'] == hospital_id]
        return render_template('hospital_details.html', 
                             hospital=hospital, 
                             doctors=hospital_doctors)
    return "Hospital not found", 404

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error handler"""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)