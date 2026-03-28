import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configuração da IA através da variável de ambiente do Render
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Instruções de comportamento do Agente
SYSTEM_PROMPT = """
Você é um Especialista em Segurança Digital. Sua missão é analisar mensagens suspeitas de WhatsApp.
1. Identifique se é um golpe (Phishing, Promoção Falsa, Pix Premiado).
2. Dê um nível de risco de 0 a 100%.
3. Explique o motivo em poucas palavras.
4. Use emojis e seja direto.
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
    dados = request.get_json()
    
    # Tenta extrair a mensagem de diferentes formatos que as APIs de WhatsApp enviam
    mensagem_usuario = ""
    
    try:
        # Tenta o formato padrão da Evolution API / WPPConnect
        if 'data' in dados and 'message' in dados['data']:
            msg_data = dados['data']['message']
            mensagem_usuario = msg_data.get('conversation') or \
                               msg_data.get('extendedTextMessage', {}).get('text')
        
        # Caso o formato seja mais simples (testes diretos)
        if not mensagem_usuario:
            mensagem_usuario = dados.get('message') or dados.get('text')
            
    except Exception as e:
        print(f"Erro ao processar dados recebidos: {e}")

    # Se não encontrar texto, ignora para não dar erro no Gemini
    if not mensagem_usuario:
        return jsonify({"status": "recebido", "aviso": "nenhum texto detectado"}), 200

    # Envia para o Gemini analisar
    try:
        resultado = model.generate_content(mensagem_usuario)
        return jsonify({
            "status": "sucesso",
            "analise": resultado.text
        }), 200
    except Exception as e:
        return jsonify({"status": "erro", "detalhe": str(e)}), 500

if __name__ == "__main__":
    # O Render define a porta automaticamente na variável de ambiente PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)