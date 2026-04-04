const wppconnect = require('@wppconnect-team/wppconnect')
const axios = require('axios')

// 🔥 Criação do cliente com configurações compatíveis com Hostzera
wppconnect.create({
  session: 'antigolpe-session',
  headless: true,
  useChrome: false,
  browserArgs: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--no-first-run',
    '--no-zygote',
    '--single-process'
  ]
})
.then(client => start(client))
.catch(err => console.log('Erro ao iniciar:', err))


// 🚀 Função principal
function start(client) {

  console.log("✅ Bot iniciado com sucesso!")

  client.onMessage(async (message) => {

    // Evita mensagens vazias ou de grupo (opcional)
    if (!message.body || message.isGroupMsg) return

    console.log("📩 Mensagem recebida:", message.body)

    try {
      const response = await axios.post(
        "https://meu-agente-antigolpe.onrender.com",
        {
          text: message.body,
          from: message.from
        }
      )

      const resposta = response.data.resposta || "⚠️ Não consegui analisar."

      await client.sendText(message.from, resposta)

    } catch (err) {
      console.log("❌ Erro ao chamar API:", err.message)

      await client.sendText(
        message.from,
        "⚠️ Erro ao analisar mensagem. Tente novamente."
      )
    }
  })
}