import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from groq import Groq
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "billonario_master_777")
CORS(app)

# --- Configuración Google Login ---
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# --- Cerebro IA ---
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def index():
    user = session.get('user')
    return render_template("dashboard.html", user=user)

@app.route('/login')
def login():
    return google.authorize_redirect(url_for('authorize', _external=True))

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    session['user'] = user_info['email']
    return redirect(url_for('index'))

@app.route("/chat", methods=["POST"])
def chat():
    try:
        if 'user' not in session:
            return jsonify({"respuesta": "Inicia sesión para activar la terminal financiera."})
        mensaje = request.json.get("mensaje")
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"Asistente financiero de {session['user']}. Portfolio: $10,000."},
                {"role": "user", "content": mensaje}
            ]
        )
        return jsonify({"respuesta": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"respuesta": f"Error: {str(e)}"})

if __name__ == "__main__":
    # Render usa el puerto 10000; si no está, usa el 5000
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)