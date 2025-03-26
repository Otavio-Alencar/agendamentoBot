from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pathlib import Path
import json
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Eu sou seu bot")

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá, Mundo! 🚀")

async def agendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    agendamentos = []

    arquivo = Path('agendamentos.txt')
    if not arquivo.exists():
        f = open("agendamentos.txt", "x")

    with open("agendamentos.txt", "r",encoding='utf-8') as linhas:
        for x in linhas:
            agendamentos.append(json.loads(x.strip()))

    data = str(context.args[0])
    hora = str(context.args[1])
    duracao= str(context.args[2])

    objeto = {
        'data': data,
        'hora': hora,
        'duracao': duracao
    }

    for agendamento in agendamentos:
        if objeto['data'] == agendamento['data'] and objeto["hora"] == agendamento['hora']:
            await update.message.reply_text("Este horário já está ocupado")
            return

    with open('agendamentos.txt','a') as file:
        file.write(json.dumps(objeto) + '\n')
        file.close()
    await update.message.reply_text("Agendamento realizado com sucesso!")
    
    


def main():

    app = ApplicationBuilder().token("7919020982:AAGYNoGmvsk6aCOtyFqYUBkNz-TZBkVUbbc").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("agendar", agendar))
    app.run_polling()
if __name__ == "__main__":
    main()