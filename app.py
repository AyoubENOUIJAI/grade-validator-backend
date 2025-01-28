from flask_cors import CORS

from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)
# Predefined modules by level, specialization, and semester
MODULES = {
    "CP": {
        "Semester 1": [
            "Management", "Droit général", "Comptabilité générale", "Micro-économie", "Mathématiques appliquées", "Français & Anglais", "Méthodologie de travail universitaire"
        ],
        "Semester 2": [
            "Marketing", "Droit commercial", "Travaux d’inventaire", "Macro-économie", "Statistiques et Probabilités", "Français & Anglais", "Digital-skills"
        ]
    },
    "CGE3": {
        "Gestion": {
            "Semester 1": [
                "Gestion de la production et qualité", "Supply Chain Management", "Gestion budgétaire et de trésorerie", "Gestion des ressources humaines", "Statistiques appliquées", "Français & Anglais", "Compétences digitales et informatique"
            ],
            "Semester 2": [
                "Analyse des données", "Contrôle de gestion", "Marché des capitaux", "Comptabilité des sociétés", "Algorithmes et Programmation Python", "Français & Anglais", "Responsabilité sociétale"
            ]
        },
        "Commerce": {
            "Semester 1": [
                "Gestion de la production et qualité", "Marketing stratégique", "Comportement du consommateur", "Gestion des ressources humaines", "Statistiques appliquées", "Français & Anglais", "Compétences digitales et informatique"
            ],
            "Semester 2": [
                "Analyse des données", "Marketing opérationnel", "Etude de marché", "Marketing digital et développement Web", "Algorithmes et Programmation Python", "Français & Anglais", "Responsabilité sociétale"
            ]
        }
    }
}

@app.route('/start', methods=['GET'])
def start():
    return jsonify({
        "message": "Welcome to the Grade Validator App! Please select your year:",
        "options": ["CP (1st & 2nd Year - Tronc Commun)", "CGE3 (3rd Year)", "CGE4 (4th Year)", "CGE5 (5th Year)"]
    })

@app.route('/semester', methods=['POST'])
def semester():
    data = request.get_json()
    year = data.get('year')

    if year not in MODULES:
        return jsonify({"error": "Invalid year. Please choose 'CP', 'CGE3', 'CGE4', or 'CGE5'."}), 400

    if year == "CGE3":
        return jsonify({
            "message": "Please select your specialization:",
            "options": ["Gestion", "Commerce"]
        })

    return jsonify({
        "message": "Please select the semester:",
        "options": ["Semester 1", "Semester 2"]
    })

@app.route('/modules', methods=['POST'])
def modules():
    data = request.get_json()
    year = data.get('year')
    semester = data.get('semester')
    specialization = data.get('specialization', None)

    if year == "CGE3" and specialization not in MODULES[year]:
        return jsonify({"error": "Invalid specialization for CGE3."}), 400

    try:
        if specialization:
            module_list = MODULES[year][specialization][semester]
        else:
            module_list = MODULES[year][semester]
    except KeyError:
        return jsonify({"error": "Invalid semester or data."}), 400

    return jsonify({
        "message": "Please enter the grades for the following modules:",
        "modules": module_list
    })

@app.route('/validate', methods=['POST'])
def validate_grades():
    data = request.get_json()

    year = data.get('year')
    semester = data.get('semester')
    specialization = data.get('specialization', None)
    grades = data.get('grades', {})

    if year == "CGE3" and specialization not in MODULES[year]:
        return jsonify({"error": "Invalid specialization for CGE3."}), 400

    try:
        if specialization:
            module_list = MODULES[year][specialization][semester]
        else:
            module_list = MODULES[year][semester]
    except KeyError:
        return jsonify({"error": "Invalid semester or data."}), 400

    min_eliminatory = 6 if year == "CP" else 8
    compensation_range = (6, 10) if year == "CP" else (8, 10)

    total_grades = 0
    validated_modules = []
    compensatable_modules = []
    failed_modules = []

    for module in module_list:
        if module not in grades:
            return jsonify({"error": f"Missing grades for module: {module}"}), 400

        cc = grades[module].get('cc', 0)
        exam = grades[module].get('exam', 0)
        final_grade = (cc * 0.5) + (exam * 0.5)

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

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render dynamically assigns a port
    app.run(host="0.0.0.0", port=port, debug=True)
