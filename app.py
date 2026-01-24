import os
from flask import Flask, request, jsonify, Response
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# CONFIGURACIÓN
W_ADDR = "FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp"
G_ID = "1003655956505-nh7tso7hb4acuk77489pf9p08far0d9u.apps.googleusercontent.com"

# Interfaz compacta para evitar errores de sintaxis
UI = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>QUANTUM ELITE</title>
<script src="https://accounts.google.com/gsi/client" async defer></script>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<style>
    body {{ background:#050505; color:#fff; font-family:sans-serif; text-align:center; margin:0; }}
    .h {{ padding:60px; background:radial-gradient(circle,#0a192f,#000); border-bottom:1px solid #333; }}
    .t {{ width:90%; max-width:800px; margin:20px auto; padding:20px; background:#111; border-radius:10px; border:1px solid #444; }}
    #c {{ height:250px; overflow-y:auto; text-align:left; color:#00f2ff; font-family:monospace; }}
    input {{ width:100%; padding:15px; background:#000; border:1px solid #333; color:#fff; margin-top:10px; }}
    .btn {{ padding:10px 20px; background:#00f2ff; color:#000; text-decoration:none; font-weight:bold; border-radius:5px; display:inline-block; margin:10px; }}
</style></head>
<body>
    <div style="position:fixed;top:10px;right:10px;"><div id="g_id_onload" data-client_id="{G_ID}" data-callback="hA"></div><div class="g_id_signin" data-type="icon"></div></div>
    <div class="h"><h1>QUANTUM CORE</h1><p style="color:gray;">IA & BLOCKCHAIN INDUSTRIAL</p>
    <a href="https://solscan.io/account/{W_ADDR}" target="_blank" class="btn">VER NODE</a></div>
    <div class="t"><div id="c">>> SISTEMA ACTIVO.</div><input type="text" id="i" placeholder="Requerimiento..." onkeydown="if(event.key==='Enter') exe()">
    <div id="p" style="height:200px;margin-top:20px;"></div></div>
    <script>
        function hA(r) {{ console.log("Auth OK"); }}
        Plotly.newPlot('p',[{{x:[1,2,3,4],y:[10,15,13,18],type:'scatter',line:{{color:'#00f2ff'}}}}],{{paper_bgcolor:'rgba(0,0,0,0)',plot_bgcolor:'rgba(0,0,0,0)',font:{{color:'#fff'}},margin:{{t:0,b:30,l:30,r:10}}}});
        async function exe() {{
            const i=document.getElementById('i'), c=document.getElementById('c'); if(!i.value) return;
            const m=i.value; i.value=''; c.innerHTML += `<div>> SOLICITUD: ${{m}}</div>`;
            const r=await fetch('/chat',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{mensaje:m}})}});
            const d=await r.json(); c.innerHTML += `<div style="color:#fff;">> AI: ${{d.respuesta}}</div>`;
            if(d.qr) c.innerHTML += `<img src="${{d.qr}}" style="width:150px;margin:10px;border:1px solid #00f2ff;">`;
            c.scrollTop=c.scrollHeight;
        }}
    </script>
</body></html>
"""

@app.route("/")
def index(): return Response(UI, mimetype='text/html')

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        msg = data.get("mensaje", "").lower()
        comp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":"IA Elite."},{"role":"user","content":msg}])
        res = comp.choices[0].message.content
        out = {"respuesta": res}
        if any(x in msg for x in ["pago", "contratar", "solana"]):
            out["qr"] = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={W_ADDR}"
        return jsonify(out)
    except Exception as e: return jsonify({"respuesta": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))