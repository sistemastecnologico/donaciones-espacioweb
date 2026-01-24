import os
from flask import Flask, request, jsonify, Response
from groq import Groq

app = Flask(__name__)

# CONFIGURACIÓN DE SEGURIDAD Y CLIENTE
# Asegúrate de tener la variable GROQ_API_KEY en el panel de Render
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# TU IDENTIDAD FINANCIERA
WALLET_ADRESS = "FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp"
WALLET_LINK = f"https://solscan.io/account/{WALLET_ADRESS}"

# --- INTERFAZ DE LUJO (HTML/CSS) ---
HTML_MASTER = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premium AI - Billionaire Station</title>
    <style>
        body {{ background: #000; color: #d4af37; font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }}
        .container {{ width: 90%; max-width: 800px; background: #050505; border: 1px solid #d4af37; border-radius: 20px; padding: 30px; box-shadow: 0 0 50px rgba(212, 175, 55, 0.15); text-align: center; }}
        .header {{ margin-bottom: 20px; }}
        .btn-gold {{ background: linear-gradient(45deg, #d4af37, #f9f295); color: #000; padding: 15px 30px; border: none; border-radius: 50px; cursor: pointer; font-weight: bold; font-size: 1.1em; transition: 0.3s; margin-bottom: 20px; text-decoration: none; display: inline-block; }}
        .btn-gold:hover {{ transform: scale(1.05); box-shadow: 0 0 20px #d4af37; }}
        #chat-display {{ height: 350px; overflow-y: auto; text-align: left; background: #0a0a0a; border-radius: 10px; padding: 20px; margin-bottom: 20px; border: 1px solid #222; color: #fff; line-height: 1.6; font-family: 'Courier New', monospace; }}
        .input-area {{ position: relative; }}
        input {{ width: 100%; background: #111; border: 1px solid #333; color: #fff; padding: 15px; border-radius: 10px; outline: none; box-sizing: border-box; font-size: 1em; }}
        input:focus {{ border-color: #d4af37; }}
        .qr-img {{ margin-top: 15px; border: 5px solid #fff; border-radius: 10px; width: 180px; }}
        .stat-img {{ margin-top: 15px; border-radius: 10px; max-width: 100%; border: 1px solid #d4af37; }}
        small {{ color: #666; display: block; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <a href="{WALLET_LINK}" target="_blank" class="btn-gold">INVERTIR EN EL PROYECTO (USDC SOLANA)</a>
            <h1 style="margin:0; letter-spacing: 2px;">ELITE AI CONSULTANCY</h1>
            <p style="color: #888; margin: 5px 0;">Socio Tecnológico para Mentes de Alto Patrimonio</p>
        </div>
        <div id="chat-display">>> Sistema en línea. Esperando instrucciones estratégicas...</div>
        <div class="input-area">
            <input type="text" id="userInput" placeholder="Escriba su consulta o solicite gráficos..." onkeydown="if(event.key==='Enter') send()">
        </div>
        <small>Powered by Llama 3.3 70B & Solana Network</small>
    </div>

    <script>
        async function send() {{
            const input = document.getElementById('userInput');
            const display = document.getElementById('chat-display');
            const val = input.value;
            if(!val) return;

            display.innerHTML += `<div style="color: #d4af37; margin-bottom: 10px;"><b>Usted:</b> ${{val}}</div>`;
            input.value = '';
            display.scrollTop = display.scrollHeight;

            try {{
                const res = await fetch('/chat', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ mensaje: val }})
                }});
                const data = await res.json();
                
                display.innerHTML += `<div style="margin-bottom: 15px;"><b>IA:</b> ${{data.respuesta}}</div>`;
                
                if(data.qr) {{
                    display.innerHTML += `<div><img src="${{data.qr}}" class="qr-img"><br><small>${{data.address}}</small></div>`;
                }}
                
                if(data.imagen) {{
                    display.innerHTML += `<div><img src="${{data.imagen}}" class="stat-img"></div>`;
                }}
                
                display.scrollTop = display.scrollHeight;
            }} catch (e) {{
                display.innerHTML += `<div style="color: red;">Error de conexión con el núcleo de la IA.</div>`;
            }}
        }}
    </script>
</body>
</html>
"""

# --- LÓGICA DEL SERVIDOR (BACKEND) ---

@app.route("/")
def index():
    return Response(HTML_MASTER, mimetype='text/html')

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_msg = data.get("mensaje", "").lower()
        
        # EL CEREBRO DE LA IA
        system_prompt = (
            "Eres un Consultor Senior de Élite. Tu tono es sofisticado, sumamente educado y visionario. "
            "Ayudas a billonarios con estrategias de medicina, ciencia y finanzas. "
            "Si el usuario desea apoyar, invertir o donar, explícale que aceptamos USDC en la red Solana "
            f"en la dirección: {WALLET_ADRESS}. Sé persuasivo y elegante."
        )
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_msg}]
        )
        ai_response = completion.choices[0].message.content

        response_data = {"respuesta": ai_response}

        # DETECCIÓN DE PAGO (GENERA QR)
        pago_keywords = ["pagar", "donar", "invertir", "apoyar", "usdc", "solana", "wallet", "dinero"]
        if any(kw in user_msg for kw in pago_keywords):
            response_data["qr"] = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={WALLET_ADRESS}"
            response_data["address"] = WALLET_ADRESS

        # GENERADOR DE IMÁGENES ÚTILES (ESTADÍSTICAS)
        img_keywords = ["imagen", "grafico", "estadistica", "analisis", "mapa", "esquema"]
        if any(kw in user_msg for kw in img_keywords):
            # Usamos un motor de generación visual de datos
            response_data["imagen"] = f"https://pollinations.ai/p/{user_msg}_financial_luxury_infographic?width=1024&height=768&nologo=true"

        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({"respuesta": f"Disculpe la interrupción, mi núcleo está en mantenimiento: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)