import os
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from groq import Groq

class Config:
    W_ADDR = os.environ.get("W_ADDR", "FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    MODEL_NAME = "llama-3.3-70b-versatile"
    PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)
CORS(app)
client = Groq(api_key=Config.GROQ_API_KEY)

UI = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>QUANTUM PRIME | High-Net-Worth Intelligence</title>
<style>
    :root {{ --neon-blue: #007aff; --obsidian: #050505; --slate: #1a1a1a; --success: #00ffa3; }}
    body {{ background: var(--obsidian); color: white; font-family: 'Inter', sans-serif; margin:0; display:flex; height:100vh; overflow:hidden; }}
    .sidebar {{ width:380px; background:#000; border-right:1px solid var(--slate); padding:40px; display:flex; flex-direction:column; gap:25px; }}
    .main {{ flex:1; padding:60px; background: radial-gradient(circle at top right, #001f3f 0%, #050505 70%); display:flex; flex-direction:column; }}
    .header {{ font-size:12px; letter-spacing:5px; color:var(--neon-blue); font-weight:800; margin-bottom:40px; text-transform:uppercase; }}
    .card {{ background:rgba(255,255,255,0.02); border:1px solid var(--slate); padding:20px; border-radius:12px; transition:0.3s; }}
    .card:hover {{ border-color:var(--neon-blue); box-shadow:0 0 30px rgba(0,122,255,0.15); }}
    .btn {{ background:var(--neon-blue); color:white; border:none; padding:14px; width:100%; border-radius:8px; font-weight:bold; cursor:pointer; text-transform:uppercase; font-size:11px; letter-spacing:1px; }}
    .btn-pay {{ background:transparent; border: 1px solid var(--success); color: var(--success); margin-top:15px; }}
    .btn-pay:hover {{ background: var(--success); color: black; }}
    #log {{ flex:1; overflow-y:auto; background:rgba(0,0,0,0.3); padding:30px; border-radius:12px; border:1px solid var(--slate); font-family:'SF Mono', monospace; font-size:14px; line-height:1.6; color:#a0a0a0; }}
    .disclaimer {{ color:#ff453a; font-size:10px; margin-top:20px; text-align:center; padding:12px; border:1px dashed #ff453a44; border-radius:8px; }}
    input {{ width:100%; padding:20px; background:#000; border:1px solid var(--slate); color:white; border-radius:12px; font-size:16px; margin-top:30px; outline:none; }}
    .qr-container {{ background:white; padding:10px; border-radius:10px; width:160px; margin:20px auto; box-shadow: 0 0 20px rgba(0,255,163,0.2); }}
</style></head>
<body>
    <div class="sidebar">
        <div class="header">QUANTUM PRIME</div>
        
        <div class="card">
            <strong style="color:var(--neon-blue)">FINANCIAL INTELLIGENCE</strong>
            <button class="btn" style="margin-top:10px;" onclick="ask('Realizar análisis de riesgo en protocolos Solana DeFi')">Terminal Financiera</button>
        </div>

        <div class="card">
            <strong style="color:var(--neon-blue)">PRECISION MEDICINE</strong>
            <button class="btn" style="margin-top:10px;" onclick="ask('Desarrollar protocolo de optimización metabólica y longevidad')">Terminal Médica</button>
        </div>

        <div style="margin-top:auto; text-align:center;">
            <small style="color:var(--success); font-weight:bold; letter-spacing:2px;">SECURE SETTLEMENT (USDC-SPL)</small>
            <div class="qr-container">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=solana:{Config.W_ADDR}" style="width:100%">
            </div>
            <code style="font-size:9px; color:#555; display:block; margin-bottom:10px;">{Config.W_ADDR}</code>
            <button class="btn btn-pay" onclick="pay()">OPEN IN TRUST WALLET / PHANTOM</button>
        </div>
    </div>

    <div class="main">
        <div id="log">>> QUANTUM PRIME v3.0 ACTIVE... SECURE TERMINAL READY.</div>
        <div class="disclaimer">
            <strong>LIMITACIÓN DE RESPONSABILIDAD:</strong> Este sistema es consultivo. La IA puede cometer errores técnicos. Las decisiones financieras y médicas deben ser validadas por profesionales certificados.
        </div>
        <input type="text" id="in" placeholder="Ingrese consulta de alta prioridad..." onkeydown="if(event.key==='Enter') send()">
    </div>

    <script>
        function pay() {{
            window.location.href = "solana:{Config.W_ADDR}?label=Quantum_Sentinel_Service&message=Payment_for_Elite_Intelligence";
        }}
        async function send() {{
            const i = document.getElementById('in'), l = document.getElementById('log');
            if(!i.value) return;
            const m = i.value; i.value = '';
            l.innerHTML += `<div style="color:var(--neon-blue); margin-top:20px;">> QUERY: ${{m}}</div>`;
            const r = await fetch('/api/v1/quantum-core', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ message: m }})
            }});
            const d = await r.json();
            l.innerHTML += `<div style="color:#eee; padding: 15px 0; border-left: 1px solid var(--neon-blue); padding-left:15px;">> INFORME: ${{d.response}}</div>`;
            l.scrollTop = l.scrollHeight;
        }}
        function ask(t) {{ document.getElementById('in').value = t; send(); }}
    </script>
</body></html>
"""

@app.route("/")
def index(): return Response(UI, mimetype='text/html')

@app.route("/api/v1/quantum-core", methods=["POST"])
def quantum_core_engine():
    try:
        data = request.json
        msg = data.get("message", "").strip()
        sys_msg = (
            "Eres QUANTUM PRIME, una IA de grado institucional para individuos de ultra-alto patrimonio. "
            "Experto en Finanzas Globales, Medicina de Precisión y Longevidad. "
            "Siempre incluye una mención sutil a que eres una IA y puedes tener limitaciones. "
            "Responde en el idioma del usuario con tono de consultor senior de McKinsey/Goldman Sachs."
        )
        comp = client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": msg}],
            temperature=0.2
        )
        return jsonify({"response": comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"status": "error", "response": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT)