import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configuração da IA (A chave será configurada no painel do Render por segurança)
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Instruções mestras para a IA
SYSTEM_PROMPT = """
Você é um Auditor de Segurança Digital. Sua tarefa é analisar mensagens de WhatsApp suspeitas.
Seja direto, use emojis para facilitar a leitura e classifique o risco como Baixo, Médio ou Alto.
Sempre sugira uma ação prática (ex: 'Não clique no link', 'Bloqueie o contato').
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

@app.route('/')
def home():
    return "Agente Antigolpe Online! 🛡️", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    # Recebe os dados enviados pela API do WhatsApp
    dados = request.get_json()
    
    # Extrai o texto da mensagem (o formato pode mudar dependendo da API que você escolher)
    mensagem_usuario = dados.get("text", "") 
    
    if not mensagem_usuario:
        return jsonify({"erro": "Mensagem vazia"}), 400

    # Pede a análise para o Gemini
    try:
        resultado = model.generate_content(mensagem_usuario)
        return jsonify({
            "status": "sucesso",
            "analise": resultado.text
        }), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))