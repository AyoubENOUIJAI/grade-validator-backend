from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/module")
def module():
    return jsonify({"message": "Module route is working!"})

@app.route("/start")
def start():
    return jsonify({"message": "Start route is working!"})

# Predefined modules by year, specialization, and semester
MODULES = {
    "CP1": {
        "Semester 1": [
            "Management", "Droit général", "Comptabilité générale", "Micro-économie",
            "Mathématiques appliquées", "Français & Anglais", "Méthodologie de travail universitaire"
        ],
        "Semester 2": [
            "Marketing", "Droit commercial", "Travaux d'inventaire", "Macro-économie",
            "Statistiques et Probabilités", "Français & Anglais", "Digital-skills"
        ]
    },
    "CP2": {
        "Semester 1": [
            "Commerce et logistique", "Droit des affaires", "Comptabilité de gestion", 
            "Economie internationale", "Mathématiques et décisions financières", 
            "Français & Anglais", "Culture et art skills"
        ],
        "Semester 2": [
            "Théorie des organisations", "Fiscalité de l'entreprise", "Gestion financière",
            "Economie monétaire et techniques bancaires", "Systèmes d'information et bases de données",
            "Français & Anglais", "Soft-skills: Développement personnel"
        ]
    },
    "CGE3": {
        "Gestion": {
            "Semester 1": [
                "Gestion de la production et qualité", "Supply Chain Management", "Gestion budgétaire et de trésorerie",
                "Gestion des ressources humaines", "Statistiques appliquées", "Français & Anglais", "Compétences digitales"
            ],
            "Semester 2": [
                "Analyse des données", "Contrôle de gestion", "Marché des capitaux", 
                "Comptabilité des sociétés", "Algorithmes et Programmation Python", "Français & Anglais", "Responsabilité sociétale"
            ]
        },
        "Commerce": {
            "Semester 1": [
                "Gestion de la production et qualité", "Marketing stratégique", "Comportement du consommateur",
                "Gestion des ressources humaines", "Statistiques appliquées", "Français & Anglais", "Compétences digitales"
            ],
            "Semester 2": [
                "Analyse des données", "Marketing opérationnel", "Etude de marché",
                "Marketing digital et développement Web", "Algorithmes et Programmation Python", "Français & Anglais", "Responsabilité sociétale"
            ]
        }
    },
    "CGE4": {
        "Gestion": {
            "Finance": {
                "Semester 1": ["Management stratégique", "Evaluation des entreprises", "Finance internationale", "Stage d'approfondissement", "Français & Anglais", "Intelligence artificielle"],
                "Semester 2": ["Simulation de gestion et ERP", "Ingénierie financière", "Audit et gestion des risques financiers", "Stratégies financières avancées", "IA appliquée Fintech", "Français & Anglais", "Soft Skills"]
            },
            "Audit": {
                "Semester 1": ["Management stratégique", "Contrôle de gestion avancé", "Audit interne avancé", "Stage d'approfondissement", "Français & Anglais", "Intelligence artificielle"],
                "Semester 2": ["Audit comptable", "Gestion avancée des risques", "Audit des SI", "Méthodes quantitatives avancées", "Français & Anglais", "Soft Skills"]
            }
        },
        "Commerce": {
            "Marketing": {
                "Semester 1": ["Management stratégique", "CRM et Branding", "Marketing stratégique avancé", "Stage approfondi", "Français & Anglais", "Digital marketing avancé"],
                "Semester 2": ["Stratégies de Distribution", "Merchandising avancé", "Data Analytics", "Optimisation des ventes", "Français & Anglais", "Soft Skills"]
            }
        }
    },
    "CGE5": {
        "Gestion": {
            "Finance": {
                "Semester 1": ["Corporate Strategy", "Advanced Investment Analysis", "Risk Management", "AI in Finance", "Français & Anglais", "Leadership Skills"],
                "Semester 2": ["Capstone Project", "International Financial Strategy", "Audit for Financial Institutions", "Advanced Corporate Valuation", "Français & Anglais", "Soft Skills"]
            },
            "Audit": {
                "Semester 1": ["Corporate Strategy", "Advanced Audit Methods", "Risk Management for Corporates", "AI in Audit", "Français & Anglais", "Leadership Skills"],
                "Semester 2": ["Capstone Project", "International Audit Strategy", "Audit of Multinational Corporations", "Ethics in Audit", "Français & Anglais", "Soft Skills"]
            }
        },
        "Commerce": {
            "Marketing": {
                "Semester 1": ["Global Marketing Strategy", "Consumer Behavior Advanced", "E-commerce Innovations", "Français & Anglais", "Leadership Skills"],
                "Semester 2": ["Digital Transformation", "Big Data Analytics in Marketing", "International Trade Strategies", "Français & Anglais", "Soft Skills"]
            }
        }
    }
}

@app.route('/modules', methods=['POST'])
def modules():
    data = request.get_json()
    year = data.get('year')
    semester = data.get('semester')
    specialization = data.get('specialization', None)
    sous_filiere = data.get('sous_filiere', None)

    try:
        if year.startswith("CGE"):
            if specialization not in MODULES[year]:
                return jsonify({"error": "Invalid specialization."}), 400

            if sous_filiere:
                modules = MODULES[year][specialization][sous_filiere][semester]
            else:
                modules = MODULES[year][specialization][semester]
        else:
            modules = MODULES[year][semester]

        return jsonify({
            "message": "Modules loaded successfully.",
            "modules": modules
        })
    except KeyError:
        return jsonify({"error": "Invalid semester, specialization, or sous-filière."}), 400

@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()

    year = data.get('year')
    semester = data.get('semester')
    specialization = data.get('specialization', None)
    sous_filiere = data.get('sous_filiere', None)
    grades = data.get('grades', {})
    rattrapage_passed = data.get('rattrapage_passed', False)

    try:
        if year.startswith("CGE"):
            if specialization not in MODULES[year]:
                return jsonify({"error": "Invalid specialization."}), 400

            if sous_filiere:
                module_list = MODULES[year][specialization][sous_filiere][semester]
            else:
                module_list = MODULES[year][specialization][semester]
        else:
            module_list = MODULES[year][semester]

        validated_modules = []
        compensatable_modules = []
        failed_modules = []
        total_grades = 0

        for module in module_list:
            if module not in grades:
                return jsonify({"error": f"Missing grades for module: {module}"}), 400

            cc = grades[module].get('cc', 0)
            exam = grades[module].get('exam', 0)
            final_grade = (cc * 0.5) + (exam * 0.5)

            if rattrapage_passed:
                if final_grade >= 10:
                    validated_modules.append(module)
                elif final_grade >= 8:
                    compensatable_modules.append(module)
                else:
                    failed_modules.append(module)
            else:
                if final_grade < 10 and final_grade >= 8:
                    compensatable_modules.append(module)
                elif final_grade < 8:
                    failed_modules.append(module)
                else:
                    validated_modules.append(module)

            total_grades += final_grade

        average = total_grades / len(module_list)
        semester_validated = average >= 10 and len(failed_modules) == 0

        return jsonify({
            "validated_modules": validated_modules,
            "compensatable_modules": compensatable_modules,
            "failed_modules": failed_modules,
            "average": average,
            "semester_validated": semester_validated
        })

    except KeyError:
        return jsonify({"error": "Invalid data provided."}), 400
print(app.url_map)

if __name__ == '__main__':
import os

port = int(os.environ.get("PORT", 10000))  # Render assigns PORT dynamically
app.run(host="0.0.0.0", port=port, debug=True)
