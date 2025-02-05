from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_jwt_extended import (
    create_access_token, get_jwt_identity, get_jwt, jwt_required, JWTManager
)
from datetime import timedelta

app = Flask(__name__)

# Configuration du module JWT
app.config["JWT_SECRET_KEY"] = "Ma_clé_secrete"  # Clé secrète pour le JWT
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Token valide 1h

jwt = JWTManager(app)

# Simuler une base de données des utilisateurs
users = {
    "test": {"password": "test", "role": "user"},
    "admin": {"password": "admin", "role": "admin"}
}

@app.route('/')
def home():
    return render_template('accueil.html')

# Route pour afficher la page de connexion
@app.route('/login-page', methods=["GET"])
def login_page():
    return render_template('login.html')

# Route API de login (renvoie un JWT)
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username not in users or users[username]["password"] != password:
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401

    role = users[username]["role"]  # Récupération du rôle
    access_token = create_access_token(identity=username, additional_claims={"role": role})
    
    return jsonify(access_token=access_token)

# Route protégée nécessitant un JWT valide
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Route accessible uniquement aux admins
@app.route("/admin", methods=["GET"])
@jwt_required()
def admin():
    claims = get_jwt()  # Récupère les données du JWT
    if claims.get("role") != "admin":
        return jsonify({"msg": "Accès interdit"}), 403

    return jsonify({"msg": "Bienvenue, administrateur !"})

if __name__ == "__main__":
    app.run(debug=True)
