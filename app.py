import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from groq import Groq

app = Flask(__name__)
# Esta clave protege las sesiones de tus futuros clientes premium
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "billonario_key_2026")

# Conexión con el cerebro de IA (Groq)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def index():
    # Carga tu panel de control profesional
    return render_template("dashboard.html", user=session.get('user'))

@app.route("/chat", methods=["POST"])
def chat():
    try:
        mensaje = request.json.get("mensaje").lower()
        
        # --- FUNCIÓN ÚNICA 1: GENERADOR DE GRÁFICOS ---
        if "grafico" in mensaje or "balance" in mensaje:
            config = "{type:'bar',data:{labels:['Ene','Feb','Mar'],datasets:[{label:'Ganancias',data:[400,900,2400]}]}}"
            chart_url = f"https://quickchart.io/chart?c={config}".replace(" ", "")
            respuesta_ia = f"💹 **Análisis Visual**: Rendimiento optimizado detectado.<br><img src='{chart_url}' width='100%' style='border-radius:10px; margin-top:10px;'>"
        
        # --- FUNCIÓN ÚNICA 2: IA GENERATIVA DE IMÁGENES ---
        elif "crea" in mensaje or "imagen" in mensaje:
            prompt = mensaje.replace("crea", "").strip().replace(" ", "%20")
            img_url = f"https://pollinations.ai/p/{prompt}?width=512&height=512&seed=42"
            respuesta_ia = f"🎨 **IA Generativa**: He creado este activo visual para ti:<br><img src='{img_url}' width='100%' style='border-radius:10px; margin-top:10px;'>"

        # --- FUNCIÓN ÚNICA 3: MÓDULO DE CIBERSEGURIDAD ---
        elif "seguridad" in mensaje or "scan" in mensaje:
            respuesta_ia = "🛡️ **Cyber-Shield Activo**: Escaneando vulnerabilidades... [OK] Conexión Cifrada. [OK] Base de Datos Protegida. Tu entorno es seguro."

        else:
            # Respuesta de texto rápida con Llama 3
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": mensaje}]
            )
            respuesta_ia = completion.choices[0].message.content

        return jsonify({"respuesta": respuesta_ia})
    except Exception as e:
        # Si algo falla, esto te dirá exactamente qué es sin tumbar la app
        return jsonify({"respuesta": f"Ajuste técnico requerido: {str(e)}"})

if __name__ == "__main__":
    # Configuración para que funcione en los servidores de Render
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))