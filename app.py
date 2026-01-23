import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from groq import Groq
from authlib.integrations.flask_client import OAuth
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# --- CONFIGURACIÓN DE SEGURIDAD PROFESIONAL ---
# Esto permite que el login funcione correctamente en Render (HTTPS)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "vault_security_ultra_2026")
CORS(app)

# --- SISTEMA DE IDENTIDAD (OAuth 2.0) ---
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# --- CEREBRO DE IA (Groq Llama 3.3) ---
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def index():
    user = session.get('user')
    return render_template("dashboard.html", user=user)

@app.route('/login')
def login():
    # Redirección segura para el mercado global
    return google.authorize_redirect(url_for('authorize', _external=True))

@app.route('/authorize')
def authorize():
    try:
        token = google.authorize_access_token()
        user_info = google.parse_id_token(token)
        session['user'] = user_info['email']
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error en autorización: {str(e)}"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        mensaje = request.json.get("mensaje")
        user_email = session.get('user', 'Inversionista_Anonimo')
        
        # Lógica de negocio para atraer inversores
        system_prompt = (
            f"Eres el Cerebro de una Terminal Financiera de Élite. Usuario: {user_email}. "
            "Objetivo: Maximizar capital y analizar riesgos de ciberseguridad. "
            "Portfolio: $10,000.00. Si no hay sesión, invita a activar el 'Modo de Memoria'."
        )

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": mensaje}
            ],
            temperature=0.5
        )
        return jsonify({"respuesta": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"respuesta": f"Alerta: Error de sistema {str(e)}"})

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)