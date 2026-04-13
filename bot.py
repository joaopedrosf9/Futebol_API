import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import api_futebol

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    boas_vindas = "Olá! Sou o seu Bot de Futebol ⚽\nDigite /tabela para ver o Top 10 do Brasileirão!"
    await update.message.reply_text(boas_vindas)

async def tabela(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Buscando a tabela atualizada na API, um momento... ⏳")
    
    try:
        resultado = api_futebol.buscar_classificacao_brasileirao()
        
        if resultado:
            tabela_dados = resultado['standings'][0]['table']
            mensagem = "🏆 Tabela do Brasileirão 🏆\n\n"
            
            for posicao in tabela_dados[:10]:
                nome = posicao['team']['name'] 
                pontos = posicao['points']
                jogos = posicao['playedGames']
                
                mensagem += f"{posicao['position']}º {nome} | {pontos} pts | {jogos} J\n"
                
            await update.message.reply_text(mensagem)
        else:
            await update.message.reply_text("Puxa, não consegui acessar a tabela agora. A API pode estar fora do ar!")

    except Exception as erro:
        print(f"ERRO FATAL NA FUNÇÃO TABELA: {erro}")
        await update.message.reply_text("Deu um erro no meu sistema interno! 🛠️ O desenvolvedor precisa olhar o terminal.")

if __name__ == '__main__':
    print("Iniciando o bot...")
    
    token = os.getenv("TELEGRAM_TOKEN")
    
    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tabela", tabela))
    
    print("Bot online! Vá para o Telegram e mande um /start")
    
    app.run_polling()