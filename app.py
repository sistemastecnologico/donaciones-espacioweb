from flask import Flask, render_template, request, session, jsonify
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = 'bitcoin2026'
csrf = CSRFProtect(app)
CORS(app)

# --- CONFIGURACIÓN DE IA (TU LLAVE REAL) ---
API_KEY_REAL = "AIzaSyAFLGjZUy4E2qXYwRk3q4AwNbtNRWGk3c8"
genai.configure(api_key=API_KEY_REAL)
ia_brain = genai.GenerativeModel('gemini-1.5-flash')

# --- VARIABLES Y WALLET ---
balance_usd = 10000.00
wallets = {'BTC': 0.0, 'ETH': 0.0}
donation_address = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"

# --- RUTA DEL CEREBRO IA ---
@app.route('/chat', methods=['POST'])
@csrf.exempt 
def chat_ia():
    try:
        data = request.json
        pregunta = data.get("mensaje")
        contexto = f"Eres una IA de élite. Ayudas gratis. Donaciones BTC: {donation_address}"
        response = ia_brain.generate_content(contexto + ": " + pregunta)
        return jsonify({"respuesta": response.text}) # Corregido de .lexl a .text
    except Exception as e:
        return jsonify({"respuesta": "Error en el cerebro. Intenta de nuevo."})

# --- RUTA DASHBOARD ---
@app.route("/")
def dashboard():
    csrf_token = generate_csrf()
    return render_template('dashboard.html', 
                           balance=balance_usd, # Corregido de balance-balance_usd a balance=balance_usd
                           wallets=wallets, 
                           donation_address=donation_address, 
                           csrf_token=csrf_token)

if __name__ == '__main__':
    # Corregido: port=5000 y host='0.0.0.0'
    app.run(host='0.0.0.0', port=5000, debug=True)