import os
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from groq import Groq

# =========================
# CONFIGURACIÓN SOLANA USDC
# =========================
W_ADDR = "FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp"

# USDC MINT OFICIAL EN SOLANA (CORREGIDO)
USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

# =========================
# APP
# =========================
app = Flask(__name__)
CORS(app)

# =========================
# GROQ CLIENT (SEGURO)
# =========================
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("Falta la variable de entorno GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# =========================
# HTML UI
# =========================
def get_html_content():
    h = """
    <html>
    <head>
        <meta charset="utf-8">
        <title>QUANTUM PRIME</title>
        <style>
            body { background:#000; color:#0f0; font-family:monospace; padding:25px }
            .c { border:1px solid #0f0; padding:20px; border-radius:10px }
            .btn {
                display:block; background:#0f0; color:#000;
                padding:15px; text-align:center; text-decoration:none;
                font-weight:bold; margin-top:20px; border-radius:5px
            }
        </style>
    </head>
    <body>
        <div class="c">
            <h2>QUANTUM PRIME v12</h2>
            <p>ESTADO: SISTEMA ACTIVO · IA + SEGURIDAD</p>

            <a class="btn"
               href="solana:{addr}?spl-token={mint}">
               PAGAR $6,500 USDC
            </a>
        </div>

        <div id="log"
             style="height:250px; overflow:auto; margin-top:20px;
                    border:1px solid #333; padding:10px"></div>

        <input id="in"
               style="width:100%; background:#000; color:#0f0;
                      border:1px solid #0f0; padding:15px; margin-top:10px"
               placeholder="Escriba comando de seguridad..."
               onkeydown="if(event.key==='Enter') send()">

        <script>
            async function send() {
                const i = document.getElementById("in");
                const l = document.getElementById("log");
                if (!i.value) return;

                l.innerHTML += "<div>&gt; " + i.value + "</div>";

                const r = await fetch("/api/v1/quantum-core", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: i.value })
                });

                const d = await r.json();
                l.innerHTML += "<div style='color:#fff'>AI: " + d.response + "</div>";
                i.value = "";
                l.scrollTop = l.scrollHeight;
            }
        </script>
    </body>
    </html>
    """.format(addr=W_ADDR, mint=USDC_MINT)

    return h

# =========================
# ROUTES
# =========================
@app.route("/")
def index():
    return render_template_string(get_html_content())

@app.route("/api/v1/quantum-core", methods=["POST"])
def quantum_core_engine():
    try:
        data = request.get_json(silent=True) or {}
        user_msg = data.get("message", "").strip()

        if not user_msg:
            return jsonify({"response": "Comando vacío."})

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            messages=[
                {
                    "role": "system",
                    "content": "Eres QUANTUM PRIME, experto en ciberseguridad. Responde de forma técnica y clara."
                },
                {
                    "role": "user",
                    "content": user_msg
                }
            ]
        )

        return jsonify({
            "response": completion.choices[0].message.content
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "response": str(e)
        }), 500

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
