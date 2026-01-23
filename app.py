import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from groq import Groq
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
# Seguridad Industrial: Llave de cifrado para proteger sesiones de inversores
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "vault_security_ultra_2026")
CORS(app)

# --- SISTEMA DE IDENTIDAD SEGURA (Lo que vende a empresas) ---
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# --- MOTOR DE IA DE ALTA VELOCIDAD (Groq Llama 3.3) ---
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def index():
    user = session.get('user')
    # Enviamos los datos del usuario al dashboard para personalizar la experiencia
    return render_template("dashboard.html", user=user)

@app.route('/login')
def login():
    # Sistema de acceso seguro para inversionistas y usuarios premium
    return google.authorize_redirect(url_for('authorize', _external=True))

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    session['user'] = user_info['email']
    # Aquí se activaría la base de datos para ahorro de datos del cliente
    return redirect(url_for('index'))

@app.route("/chat", methods=["POST"])
def chat():
    try:
        mensaje = request.json.get("mensaje")
        user_email = session.get('user', 'Inversionista_Anonimo')
        
        # PROMPT DE INGENIERÍA FINANCIERA: Esto es lo que atrae el dinero
        system_prompt = (
            f"Eres el Cerebro de una Terminal Financiera de Élite. Usuario actual: {user_email}. "
            "Tu objetivo es maximizar el capital, analizar riesgos de ciberseguridad en transacciones "
            "y ofrecer estrategias de ahorro inteligente. Portfolio simulación: $10,000.00. "
            "Si el usuario no está logueado, responde con brillantez pero recuérdale que "
            "el 'Modo de Memoria Persistente' se activa al iniciar sesión."
        )

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": mensaje}
            ],
            temperature=0.5 # Mayor precisión para temas de dinero
        )
        return jsonify({"respuesta": completion.choices[0].message.content})
    
    except Exception as e:
        return jsonify({"respuesta": f"Alerta de Sistema: Error en protocolo de seguridad {str(e)}"})

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Configuración optimizada para servidores en la nube (Render)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)