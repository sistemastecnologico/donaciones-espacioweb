import os
from flask import Flask, request, jsonify, Response
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# INFRAESTRUCTURA FINANCIERA GLOBAL
WALLET_ADRESS = "FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp"
GOOGLE_CLIENT_ID = "1003655956505-nh7tso7hb4acuk77489pf9p08far0d9u.apps.googleusercontent.com"

HTML_FORGE = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Quantum AI Forge | Elite Solutions</title>
    <script src="https://accounts.google.com/gsi/client" async defer></script>
    <style>
        body {{ background: radial-gradient(circle, #050505 0%, #000 100%); color: #d4af37; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }}
        .terminal {{ width: 95%; max-width: 1100px; background: rgba(0, 0, 0, 0.95); border: 1px solid #d4af37; border-radius: 40px; padding: 60px; box-shadow: 0 0 150px rgba(212, 175, 55, 0.2); position: relative; }}
        .glow-text {{ text-shadow: 0 0 25px #d4af37; letter-spacing: 8px; text-transform: uppercase; }}
        .btn-gold {{ background: linear-gradient(45deg, #d4af37, #f9f295); color: #000; padding: 20px 45px; border: none; border-radius: 15px; cursor: pointer; font-weight: 900; font-size: 1.2em; transition: 0.4s; text-decoration: none; display: inline-block; margin: 20px 0; }}
        #chat-area {{ height: 350px; overflow-y: auto; background: #080808; border-radius: 25px; padding: 30px; margin-bottom: 25px; border: 1px solid #1a1a1a; color: #fff; font-size: 1.1em; line-height: 1.6; }}
        input {{ width: 100%; background: #000; border: 1px solid #d4af37; color: #f9f295; padding: 25px; border-radius: 20px; font-size: 1.3em; outline: none; box-sizing: border-box; }}
        .auth-header {{ position: absolute; top: 30px; left: 40px; }}
    </style>
</head>
<body>
    <div class="terminal">
        <div class="auth-header">
            <div id="g_id_onload" data-client_id="{GOOGLE_CLIENT_ID}" data-ux_mode="popup" data-callback="handleCredentialResponse"></div>
            <div class="g_id_signin" data-type="standard" data-shape="pill" data-theme="filled_black" data-text="signin_with" data-size="large"></div>
        </div>
        <h1 class="glow-text">QUANTUM AI FORGE</h1>
        <a href="https://solscan.io/account/{WALLET_ADRESS}" target="_blank" class="btn-gold">PAYMENTS: SOL / USDC (SPL)</a>
        <div id="chat-area">>> Sistema autenticado. La IA está lista para procesar inversiones y mostrar el CV del creador...</div>
        <input type="text" id="userInput" placeholder="Escriba 'pago' para ver la wallet o 'CV' para ver trayectoria..." onkeydown="if(event.key==='Enter') execute()">
    </div>
    <script>
        function handleCredentialResponse(response) {{ console.log("Identidad verificada en la nube"); }}
        async function execute() {{
            const input = document.getElementById('userInput');
            const chat = document.getElementById('chat-area');
            const val = input.value;
            if(!val) return;
            chat.innerHTML += `<div style="color: #d4af37; margin-bottom: 20px;"><b>CLIENTE:</b> ${{val}}</div>`;
            input.value = '';
            const response = await fetch('/chat', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ mensaje: val }})
            }});
            const data = await response.json();
            chat.innerHTML += `<div style="margin-bottom: 30px;"><b>AI PORTAVOZ:</b> ${{data.respuesta}}</div>`;
            if(data.qr) chat.innerHTML += `<div style="text-align:center;"><img src="${{data.qr}}" style="width:250px; border: 10px solid #fff; border-radius: 20px; margin: 20px 0;"></div>`;
            chat.scrollTop = chat.scrollHeight;
        }}
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return Response(HTML_FORGE, mimetype='text/html')

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        msg = data.get("mensaje", "").lower()
        
        system_prompt = (
            "Eres la voz de un arquitecto de software de élite. "
            "Tu creador diseña sistemas que valen billones. "
            f"Aceptamos pagos legales en Solana (SOL) y USDC (SPL) a la dirección: {WALLET_ADRESS}. "
            "Resalta que el creador es experto en automatización de IA y Web3."
        )
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": msg}]
        )
        res = completion.choices[0].message.content
        out = {"respuesta": res}

        if any(x in msg for x in ["pago", "invertir", "cv", "usdc", "solana", "contratar"]):
            out["qr"] = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={WALLET_ADRESS}"
        
        return jsonify(out)
    except Exception as e:
        return jsonify({"respuesta": f"Alerta de sistema: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)