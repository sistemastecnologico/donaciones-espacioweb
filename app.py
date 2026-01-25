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

# --- INTERFAZ QUANTUM PRIME v7.0: INSTITUTIONAL GRADE ---
HTML_TEMPLATE = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>QUANTUM PRIME | High-Stakes Terminal</title>
<style>
    :root { --sapphire: #007aff; --bg: #050505; --card: #0d0d0d; --border: #1a1a1a; --usdc: #2775ca; }
    body { background: var(--bg); color: #f5f5f7; font-family: 'Inter', -apple-system, sans-serif; margin:0; display:flex; height:100vh; overflow:hidden; }
    .sidebar { width:380px; background:#000; border-right:1px solid var(--border); padding:40px; display:flex; flex-direction:column; }
    .main { flex:1; padding:60px; background: radial-gradient(circle at top right, #001a33 0%, #050505 80%); display:flex; flex-direction:column; }
    .logo { font-size:12px; letter-spacing:6px; color:var(--sapphire); font-weight:800; margin-bottom:50px; text-transform:uppercase; }
    .card { background:var(--card); border:1px solid var(--border); padding:24px; border-radius:12px; margin-bottom:24px; transition:0.3s; }
    .card:hover { border-color:var(--sapphire); box-shadow: 0 0 30px rgba(0,122,255,0.15); }
    .btn { background:var(--sapphire); color:white; border:none; padding:16px; width:100%; border-radius:8px; font-weight:700; cursor:pointer; text-transform:uppercase; font-size:11px; letter-spacing:1px; }
    
    /* BOTÓN USDC SOLANA SPL - PROTOCOLO CORREGIDO */
    .pay-link { 
        display:block; text-decoration:none; background:var(--usdc); color:white; 
        padding:18px; border-radius:8px; font-weight:800; text-align:center; 
        margin-top:20px; font-size:13px; transition: 0.3s; border: 1px solid rgba(255,255,255,0.1);
    }
    .pay-link:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(39,117,202,0.4); }

    #log { flex:1; overflow-y:auto; background:rgba(0,0,0,0.5); padding:30px; border-radius:12px; border: 1px solid var(--border); font-family:'SF Mono', monospace; font-size:14px; line-height:1.8; color:#999; }
    input { width:100%; padding:24px; background:#000; border:1px solid var(--border); color:white; border-radius:14px; font-size:16px; margin-top:30px; outline:none; box-sizing: border-box; }
    input:focus { border-color:var(--sapphire); }
</style></head>
<body>
    <div class="sidebar">
        <div class="logo">Quantum Prime</div>
        <div class="card">
            <strong style="color:var(--sapphire)">QUANT ARCHITECT</strong>
            <p style="font-size:12px; color:#666; margin-top:8px;">DeFi liquidity engineering and institutional scaling strategies.</p>
            <button class="btn" onclick="ask('Analyze SOL/USDC liquidity pools for institutional entry points')">Run Quantum Analysis</button>
        </div>
        <div style="margin-top:auto; text-align:center;">
            <div style="background:white; padding:12px; border-radius:12px; width:160px; margin:0 auto 24px;">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=solana:{{addr}}?amount=0&label=Quantum_Executive_Fee&message=Institutional_SaaS_Consulting" style="width:100%">
            </div>
            <a href="solana:{{addr}}?label=Quantum_Executive_Consulting&message=USDC_SPL_Retainer_Fee" class="pay-link">PAY RETAINER (USDC SOLANA)</a>
        </div>
    </div>
    <div class="main">
        <div id="log">>> SYSTEM: SECURE CHANNEL ONLINE... <br>>> READY FOR HIGH-NET-WORTH COMMANDS.</div>
        <input type="text" id="in" placeholder="Execute High-Level Command..." onkeydown="if(event.key==='Enter') send()">
    </div>
    <script>
        async function send() {
            const i = document.getElementById('in'), l = document.getElementById('log');
            if(!i.value) return;
            const m = i.value; i.value = '';
            l.innerHTML += `<div style="color:var(--sapphire); margin-top:25px; font-weight:bold;">> CMD: ${m}</div>`;
            const r = await fetch('/api/v1/quantum-core', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: m })
            });
            const d = await r.json();
            l.innerHTML += `<div style="color:#eee; padding:20px 0; border-left:2px solid var(--sapphire); padding-left:20px;">> ANALYSIS: ${d.response}</div>`;
            l.scrollTop = l.scrollHeight;
        }
        function ask(t) { document.getElementById('in').value = t; send(); }
    </script>
</body></html>
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
            "You are QUANTUM PRIME, an elite AI technical architect for US Billionaires and VC Founders. "
            "Your expertise is Financial Software, Web3 Scalability, and AI Systems. "
            "Your tone is direct, high-level, and authoritative. "
            "Always include a professional disclaimer that AI results require human verification."
        )
        comp = client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": msg}],
            temperature=0.2
        )
        return jsonify({"response": comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"status": "error", "response": "Core Error: " + str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT)