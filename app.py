from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def analisar_mensagem(texto):
    prompt = f"""
    Você é um sistema antifraude avançado.

    Analise a mensagem com base em:
    - engenharia social
    - urgência
    - promessa de ganho
    - links suspeitos
    - pedido de dados pessoais

    Responda EXATAMENTE neste formato:

    🚨 Golpe detectado: (SIM ou NÃO)

    🔎 Motivos:
    - Liste de 2 a 4 motivos claros

    📊 Nível de risco: (0 a 10)

    🧠 Tipo de golpe (se houver):
    (ex: phishing, falso prêmio, falso suporte, golpe do pix)

    🛡️ Recomendação:
    - Dê uma recomendação prática

    Mensagem:
    "{texto}"
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

    body = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, json=body)
        data = response.json()

        resposta = data["candidates"][0]["content"]["parts"][0]["text"]
        return resposta

    except Exception as e:
        print("Erro na IA:", e)
        return "⚠️ Não consegui analisar a mensagem. Tente novamente."


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    if not data or "text" not in data:
        return jsonify({"erro": "Requisição inválida"}), 400

    texto = data.get("text")

    print("📩 Mensagem recebida:", texto)

    resposta = analisar_mensagem(texto)

    return jsonify({
        "resposta": resposta
    })


@app.route('/')
def home():
    return "✅ Servidor do agente antigolpe está rodando!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)