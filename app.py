# Modify the backend `app.py` to fix module fetching issues

fixed_backend_code = """\
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
            "Théorie des organisations", "Fiscalité de l'entreprise", "Gestion budgétaire",
            "Economie du développement", "Modélisation et aide à la décision", 
            "Français & Anglais", "Ethique et responsabilité sociétale"
        ]
    },
    "CGE3": {
        "Gestion": [],
        "Commerce": []
    },
    "CGE4": {
        "Gestion": ["Finance", "Audit", "Supply Chain", "Management RH", "Management de Projet", "Business Administration"],
        "Commerce": ["Marketing", "International Trade", "Management RH", "Management de Projet", "Business Administration"]
    },
    "CGE5": {
        "Gestion": ["Finance Advanced", "Audit Advanced", "Management RH", "Management de Projet", "Business Administration"],
        "Commerce": ["Marketing Digital", "Management RH", "Management de Projet", "Business Administration"]
    }
}

@app.route('/modules', methods=['GET'])
def get_modules():
    year = request.args.get('year', '')
    specialization = request.args.get('specialization', '')

    if year in MODULES:
        if year == "CGE3":
            return jsonify(["Gestion", "Commerce"])  # Show specializations for CGE3
        elif year in ["CGE4", "CGE5"] and specialization in MODULES[year]:
            return jsonify(MODULES[year][specialization])  # Return specialization modules
        else:
            return jsonify(MODULES[year])  # Return CP1 & CP2 modules
    return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
"""

# Write the fixed code back to `app.py`
fixed_app_py_path = os.path.join(backend_project_path, "app.py")

with open(fixed_app_py_path, "w", encoding="utf-8") as file:
    file.write(fixed_backend_code)

# Confirm the fix was applied
fixed_backend_code[:1000]
