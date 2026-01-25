import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

# --- ESTRUCTURA DE CONFIGURACIÓN BANCARIA ---
class Config:
    W_ADDR = os.environ.get("W_ADDR", "FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    MODEL_NAME = "llama-3.3-70b-versatile"
    PORT = int(os.environ.get("PORT", 10000))
    DEBUG = False

# Registro de Auditoría Industrial
logging.basicConfig(level=logging.INFO, format='%(asctime)s - DAPP_SENTINEL - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app) # Permite conexión con React.js según el requerimiento
client = Groq(api_key=Config.GROQ_API_KEY)

@app.route("/api/v1/quantum-core", methods=["POST"])
def quantum_core_engine():
    try:
        data = request.json
        msg = data.get("message", "").strip()
        
        # Validación de Seguridad contra Inyección de Código
        if not msg or len(msg) > 1500:
            return jsonify({"status": "security_reject", "response": "Protocol violation: Message exceeds safety limits."}), 400

        logger.info(f"DApp Logic Executing: {msg[:40]}...")

        # SYSTEM PROMPT MULTI-DOMINIO (Finanzas, Medicina y Web3)
        sys_prompt = (
            "You are QUANTUM CORE v3.0, a Decentralized Intelligence Sentinel. "
            "Expertise: 1. Solana/Ethereum Smart Contracts & Web3.js. 2. Advanced Financial Analytics. "
            "3. Medical Diagnostic Support. 4. High-Performance Software Engineering. "
            "Instruction: Be technical, concise, and respond in the user's language."
        )

        comp = client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": msg}],
            temperature=0.2 # Precisión quirúrgica para datos críticos
        )

        res_text = comp.choices[0].message.content
        out = {"response": res_text, "status": "authorized_by_core"}

        # Puerta de Enlace de Pago Web3 Integrada
        trigger_words = ["pago", "pay", "contratar", "hire", "solana", "fee", "medical", "finance"]
        if any(word in msg.lower() for word in trigger_words):
            out["blockchain_gateway"] = {
                "qr": f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=solana:{Config.W_ADDR}",
                "network": "Solana Mainnet",
                "wallet": Config.W_ADDR,
                "memo": "DApp_Core_Service_Execution"
            }
            
        return jsonify(out)
    except Exception as e:
        logger.error(f"Critical System Breach: {str(e)}")
        return jsonify({"status": "critical_failure", "response": "Engine protocol error."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)