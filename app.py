import os
from flask import Flask, request, jsonify, render_template_string
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

# INTERFAZ DE ALTA DISPONIBILIDAD - SIN CORTES DE CÓDIGO
UI = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>QUANTUM PRIME</title>
<style>
 body{background:#020205;color:#0f0;font-family:monospace;margin:0;display:flex;height:100vh}
 .side{width:280px;background:#000;border-right:1px solid #1a1a1a;padding:25px;display:flex;flex-direction:column}
 .main{flex:1;padding:40px;display:flex;flex-direction:column}
 .card{background:#0d0d0d;border:1px solid #0f0;padding:12px;border-radius:5px;margin-bottom:10px;font-size:11px}
 .pay{display:block;text-decoration:none;background:#0f0;color:#000;padding:15px;border-radius:5px;font-weight:900;text-align:center;margin-top:20px}
 #log{flex:1;overflow-y:auto;background:rgba(0,0,0,0.9);padding:20px;border:1px solid #1a1a1a;font-size:13px}
 input{width:100%;padding:15px;background:#000;border:1px solid #0f0;color:#0f0;margin-top:15px}
</style></head><body>
<div class="side">
 <h2>QUANTUM_CORE</h2>
 <div class="card">SECTOR: CYBER-SEC<br>STATUS: ENCRYPTED</div>
 <div class="card">SECTOR: BIOMED<br>STATUS: ANALYZING</div>
 <div class="card">SECTOR: FINTECH<br>STATUS: SOL_READY</div>
 <div style="margin-top:auto;text-align:center">
  <div style="background:#fff;padding:5px;border-radius:5px;width:110px;margin:0 auto">
   <img src="https://api.qrserver.com/v1/create-qr-code/?size=110x110&data=solana:{{addr}}" style="width:100%">
  </div>
  <a href="solana:{{addr}}?label=Quantum_Premium&message=Cyber_Med_Consulting" class="pay">PAY PREMIUM</a>
 </div>
</div>
<div class="main">
 <div id="log">>> SYSTEM READY. AI ACTIVE.<br>>> NOTICE: AI MAY ERR. VERIFY ALL DATA.</div>
 <input type="text" id="in" placeholder="Enter Command..." onkeydown="if(event.key==='Enter')send()">
</div>
<script>
 async function send(){
  const i=document.getElementById('in'),l=document.getElementById('log');if(!i.value)return;const m=i.value;i.value='';
  l.innerHTML+=`<div style="color:#fff;margin-top:15px">> ${m}</div>`;
  const r=await fetch('/api/v1/quantum-core',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m})});
  const d=await r.json();l.innerHTML+=`<div>> ${d.response}</div>`;
  l.scrollTop=l.scrollHeight
 }
</script></body></html>
"""

@app.route("/")
def index(): return render_template_string(UI, addr=Config.W_ADDR)

@app.route("/api/v1/quantum-core", methods=["POST"])
def quantum_core_engine():
    try:
        data = request.json
        sys = "You are QUANTUM PRIME. Expert in Cyber-Security, Medicine, and Finance. Accurate and direct."
        comp = client.chat.completions.create(model=Config.MODEL_NAME, messages=[{"role": "system", "content": sys}, {"role": "user", "content": data.get("message", "")}], temperature=0.1)
        return jsonify({"response": comp.choices[0].message.content})
    except Exception as e: return jsonify({"status":"error","response":str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT)