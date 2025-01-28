from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Predefined modules by year, specialization, and semester
MODULES = {
    "CP1": {
        "Semester 1": [
            "Management", "Droit général", "Comptabilité générale", "Micro-économie", "Mathématiques appliquées", "Français & Anglais", "Méthodologie de travail universitaire"
        ],
        "Semester 2": [
            "Marketing", "Droit commercial", "Travaux d’inventaire", "Macro-économie", "Statistiques et Probabilités", "Français & Anglais", "Digital-skills"
        ]
    },
    "CP2": {
        "Semester 1": [
            "Commerce et logistique", "Droit des affaires", "Comptabilité de gestion", "Economie internationale", "Mathématiques et décisions financières", "Français & Anglais", "Culture et art skills"
        ],
        "Semester 2": [
            "Théorie des organisations", "Fiscalité de l’entreprise", "Gestion financière", "Economie monétaire et techniques bancaires", "Systèmes d’information et bases de données", "Français & Anglais", "Soft-skills: Développement personnel"
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
    },
    "CGE4": {
        "Gestion": {
            "Finance": {
                "Semester 1": ["Management stratégique", "Evaluation des entreprises", "Finance internationale", "Stage d’approfondissement", "Français & Anglais", "Intelligence artificielle"],
                "Semester 2": ["Simulation de gestion et ERP", "Ingénierie financière", "Audit et gestion des risques financiers", "Stratégies financières", "IA appliquée Fintech", "Français & Anglais", "Employment skills"]
            },
            "Audit": {
                "Semester 1": ["Management stratégique", "Contrôle de gestion avancé", "Audit opérationnel", "Stage d’approfondissement", "Français & Anglais", "Intelligence artificielle"],
                "Semester 2": ["Simulation de gestion et ERP", "Audit comptable et fiscal", "Audit et optimisation", "Fusions et acquisitions", "IA appliquée ", "Français & Anglais", "Employment skills"]
            }
        },
        "Commerce": {
            "Marketing": {
                "Semester 1": ["Management stratégique", "CRM et Branding", "Marketing stratégique", "Stage d’approfondissement", "Français & Anglais", "Digital competences"],
                "Semester 2": ["ERP Simulation", "Digital marketing avancé", "Marketing analytique", "Merchandising avancé", "Employment Skills"]
            }
        }
    }
}

@app.route('/validate', methods=['POST'])
def validate_grades():
    data = request.get_json()

    year = data.get('year')
    semester = data.get('semester')
    specialization = data.get('specialization', None)
    grades = data.get('grades', {})

    # Handle specialization validation
    if year.startswith('CGE') and specialization not in MODULES[year]:
        return jsonify({"error": "Invalid specialization."}), 400

    try:
        module_list = MODULES[year]
    except KeyError:
        return jsonify({"error": "Invalid semester or year."}), 400
