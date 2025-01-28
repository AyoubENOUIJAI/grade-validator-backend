from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Predefined modules by year, specialization, and semester
MODULES = {
    "CP1": {
        "Semester 1": [
            "Management", "Droit général", "Comptabilité générale", "Micro-économie",
            "Mathématiques appliquées", "Français & Anglais", "Méthodologie de travail universitaire"
        ],
        "Semester 2": [
            "Marketing", "Droit commercial", "Travaux d’inventaire", "Macro-économie",
            "Statistiques et Probabilités", "Français & Anglais", "Digital-skills"
        ]
    },
    "CP2": {
        "Semester 1": [
            "Commerce et logistique", "Droit des affaires", "Comptabilité de gestion", 
            "Économie internationale", "Mathématiques et décisions financières", 
            "Français & Anglais", "Culture et art skills"
        ],
        "Semester 2": [
            "Théorie des organisations", "Fiscalité de l’entreprise", "Gestion financière",
            "Économie monétaire et techniques bancaires", "Systèmes d’information et bases de données",
            "Français & Anglais", "Soft-skills: Développement personnel"
        ]
    }
}

@app.route('/start', methods=['GET'])
def start():
    return jsonify({
        "message": "Welcome to the Grade Validator App! Please select your year:",
        "options": ["CP1 (1st Year)", "CP2 (2nd Year)", "CGE3 (3rd Year)", "CGE4 (4th Year)", "CGE5 (5th Year)"]
    })

@app.route('/modules', methods=['POST'])
def modules():
    data = request.get_json()
    year = data.get('year')
    semester = data.get('semester')

    try:
        modules = MODULES[year][semester]
        return jsonify({
            "message": "Please enter the grades for the following modules:",
            "modules": modules
        })
    except KeyError:
        return jsonify({"error": "Invalid year or semester."}), 400

@app.route('/validate', methods=['POST'])
def validate_grades():
    data = request.get_json()

    year = data.get('year')
    semester = data.get('semester')
    grades = data.get('grades', {})

    try:
        module_list = MODULES[year][semester]
    except KeyError:
        return jsonify({"error": "Invalid year or semester."}), 400

    min_eliminatory = 6 if year.startswith("CP") else 8
    compensation_range = (6, 10) if year.startswith("CP") else (8, 10)

    total_grades = 0
    validated_modules = []
    compensatable_modules = []
    failed_modules = []

    for module in module_list:
        if module not in grades:
            return jsonify({"error": f"Missing grades for module: {module}"}), 400

        cc = grades[module].get('cc', 0)
        exam = grades[module].get('exam', 0)
        rattrapage = grades[module].get('rattrapage', False)
        final_grade = (cc * 0.5) + (exam * 0.5)

        if rattrapage:
            if final_grade < min_eliminatory:
                failed_modules.append(module)
            elif compensation_range[0] <= final_grade < 10:
                compensatable_modules.append(module)
            else:
                validated_modules.append(module)
        else:
            if final_grade < min_eliminatory:
                failed_modules.append(module)
            elif compensation_range[0] <= final_grade < 10:
                compensatable_modules.append(module)
            else:
                validated_modules.append(module)

        total_grades += final_grade

    average = total_grades / len(module_list)
    semester_validated = average >= 10 and len(failed_modules) == 0

    honors = None
    if semester_validated:
        if average >= 16:
            honors = "Très bien"
        elif average >= 14:
            honors = "Bien"
        elif average >= 12:
            honors = "Assez bien"
        elif average >= 10:
            honors = "Passable"

    result = {
        "validated_modules": validated_modules,
        "compensatable_modules": compensatable_modules,
        "failed_modules": failed_modules,
        "average": average,
        "semester_validated": semester_validated,
        "honors": honors,
    }

    return jsonify(result)

# Correct Port Binding Logic for Render
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Render dynamically assigns a port
    app.run(host="0.0.0.0", port=port, debug=True)
