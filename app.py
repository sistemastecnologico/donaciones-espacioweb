import os
from flask import Flask, request, jsonify, Response, render_template_string
from flask_cors import CORS
from groq import Groq

class Config:
    W_ADDR = "FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp"
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    MODEL_NAME = "llama-3.3-70b-versatile"
    PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)
CORS(app)
client = Groq(api_key=Config.GROQ_API_KEY)

# HTML DE GRADO INSTITUCIONAL - DISEÑO "STEALTH WEALTH"
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QUANTUM PRIME | Institutional Terminal</title>
    <style>
        :root { --accent: #007aff; --bg: #050505; --surface: #0d0d0d; --border: #1a1a1a; --success: #00ffa3; }
        body { background: var(--bg); color: #e0e0e0; font-family: 'Inter', -apple-system, sans-serif; margin:0; display:flex; height:100vh; overflow:hidden; }
        .sidebar { width:380px; background:#000; border-right:1px solid var(--border); padding:40px; display:flex; flex-direction:column; }
        .main { flex:1; padding:60px; background: radial-gradient(circle at top right, #001a33 0%, #050505 80%); display:flex; flex-direction:column; }
        .logo { font-size:12px; letter-spacing:6px; color:var(--accent); font-weight:800; margin-bottom:50px; text-transform:uppercase; }
        .card { background:var(--surface); border:1px solid var(--border); padding:24px; border-radius:12px; margin-bottom:24px; transition:0.3s; }
        .card:hover { border-color:var(--accent); box-shadow: 0 0 30px rgba(0,122,255,0.15); }
        .btn { background:var(--accent); color:white; border:none; padding:16px; width:100%; border-radius:8px; font-weight:700; cursor:pointer; text-transform:uppercase; font-size:11px; letter-spacing:1px; }
        /* BOTÓN DE PAGO SOLANA PAY (USDC SPL) */
        .pay-link { display:block; text-decoration:none; background:transparent; border:1px solid var(--success); color:var(--success); padding:18px; border-radius:8px; font-weight:800; text-align:center; margin-top:20px; font-size:13px; transition: 0.3s; }
        .pay-link:hover { background:var(--success); color:black; box-shadow: 0 0 25px rgba(0,255,163,0.3); }
        #log { flex:1; overflow-y:auto; background:rgba(0,0,0,0.5); padding:30px; border-radius:12px; border: 1px solid var(--border); font-family:'SF Mono', 'Fira Code', monospace; font-size:14px; line-height:1.8; color:#aaa; }
        .input-area { margin-top:30px; position:relative; }
        input { width:100%; padding:24px; background:#000; border:1px solid var(--border); color:white; border-radius:14px; font-size:16px; outline:none; box-sizing: border-box; }
        input:focus { border-color:var(--accent); }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo">Quantum Prime</div>
        <div class="card">
            <strong style="color:var(--accent)">FINANCIAL ENGINEERING</strong>
            <p style="font-size:12px; color:#666; margin-top:8px;">Institutional liquidity analysis & Cross-chain asset scaling.</p>
            <button class="btn" onclick="ask('Analyze SOL institutional liquidity and USDC de-peg risks')">Execute Strategy</button>
        </div>
        <div class="card">
            <strong style="color:var(--accent)">SOFTWARE ARCHITECTURE</strong>
            <p style="font-size:12px; color:#666; margin-top:8px;">High-frequency AI automation for SaaS operations.</p>
            <button class="btn" onclick="ask('Design a scalable AI infrastructure for a multi-million user dApp')">Deploy Core</button>
        </div>
        <div style="margin-top:auto; text-align:center;">
            <div style="background:white; padding:12px; border-radius:12px; width:160px; margin:0 auto 24px;">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=solana:{{addr}}" style="width:100%">
            </div>
            <a href="solana:{{addr}}?label=Quantum_Executive_Retainer&message=USDC_SPL_Institutional_Access" class="pay-link">DIRECT USDC PAYMENT (SOLANA)</a>
        </div>
    </div>
    <div class="main">
        <div id="log">>> TERMINAL v6.0 INITIALIZED... <br>>> ENCRYPTED CHANNEL ESTABLISHED. <br>>> READY FOR COMMANDS.</div>
        <div class="input-area">
            <input type="text" id="in" placeholder="Enter High-Level Commands..." onkeydown="if(event.key==='Enter') send()">
        </div>
    </div>
    <script>
        async function send() {
            const i = document.getElementById('in'), l = document.getElementById('log');
            if(!i.value) return;
            const m = i.value; i.value = '';
            l.innerHTML += `<div style="color:var(--accent); margin-top:25px; font-weight:bold;">> COMMAND: ${m}</div>`;
            try {
                const r = await fetch('/api/v1/quantum-core', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: m })
                });
                const d = await r.json();
                l.innerHTML += `<div style="color:#eee; padding:20px 0; border-left:2px solid var(--accent); padding-left:20px;">> ANALYSIS: ${d.response}</div>`;
            } catch(e) {
                l.innerHTML += `<div style="color:#ff453a;">> CONNECTION ERROR: Check API keys.</div>`;
            }
            l.scrollTop = l.scrollHeight;
        }
        function ask(t) { document.getElementById('in').value = t; send(); }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, addr=Config.W_ADDR)

@app.route("/api/v1/quantum-core", methods=["POST"])
def quantum_core_engine():
    try:
        data = request.json
        msg = data.get("message", "").strip()
        sys_msg = (
            "You are QUANTUM PRIME, an elite AI architect for US Billionaires and VC Founders. "
            "Expertise: Institutional Finance, Software Scaling, and High-Frequency Automation. "
            "Tone: Ultra-professional, technical, and direct. Always state you are an AI and require human validation."
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