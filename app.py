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

UI = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>QUANTUM</title>
<style>
 body{background:#020202;color:#eee;font-family:sans-serif;margin:0;display:flex;height:100vh}
 .side{width:280px;background:#000;border-right:1px solid #1a1a1a;padding:25px;display:flex;flex-direction:column}
 .main{flex:1;padding:40px;background:radial-gradient(circle at top right,#001a33 0%,#020202 80%);display:flex;flex-direction:column}
 .pay{display:block;text-decoration:none;background:#2775ca;color:#fff;padding:18px;border-radius:8px;font-weight:800;text-align:center;margin-top:20px;font-size:13px}
 #log{flex:1;overflow-y:auto;background:rgba(0,0,0,.5);padding:20px;border-radius:10px;border:1px solid #1a1a1a;font-family:monospace;font-size:13px;color:#999}
 input{width:100%;padding:20px;background:#000;border:1px solid #1a1a1a;color:#fff;border-radius:10px;margin-top:20px;box-sizing:border-box}
</style></head><body>
<div class="side">
 <h2 style="color:#007aff;font-size:14px">QUANTUM PRIME</h2>
 <div style="background:#0d0d0d;padding:15px;border-radius:10px;border:1px solid #1a1a1a">
  <strong>ELITE ARCHITECT</strong><p style="font-size:10px;color:#555">Asset Scaling.</p>
 </div>
 <div style="margin-top:auto;text-align:center">
  <div style="background:#fff;padding:8px;border-radius:8px;width:120px;margin:0 auto 15px">
   <img src="https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=solana:{{addr}}" style="width:100%">
  </div>
  <a href="solana:{{addr}}?label=Quantum_Fee&message=Institutional_Consulting" class="pay">OPEN WALLET</a>
 </div>
</div>
<div class="main">
 <div id="log">>> READY.</div>
 <input type="text" id="in" placeholder="Command..." onkeydown="if(event.key==='Enter')send()">
</div>
<script>
 async function send(){
  const i=document.getElementById('in'),l=document.getElementById('log');if(!i.value)return;const m=i.value;i.value='';
  l.innerHTML+=`<div style="color:#007aff;margin-top:15px">> ${m}</div>`;
  const r=await fetch('/api/v1/quantum-core',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m})});
  const d=await r.json();l.innerHTML+=`<div style="color:#eee;padding:10px 0;border-left:2px solid #007aff;padding-left:15px">> ${d.response}</div>`;
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
        comp = client.chat.completions.create(model=Config.MODEL_NAME, messages=[{"role": "system", "content": "You are QUANTUM PRIME, an elite AI for Billionaires."}, {"role": "user", "content": data.get("message", "")}], temperature=0.2)
        return jsonify({"response": comp.choices[0].message.content})
    except Exception as e: return jsonify({"status":"error","response":str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT)