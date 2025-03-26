from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pathlib import Path
import json
from datetime import datetime
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


async def consultar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    agendamentos = []
    arquivo = Path('agendamentos.txt')
    if not arquivo.exists():
        await update.message.reply_text("Não há nenhum agendamento registrado.")
        return
    with open("agendamentos.txt", "r",encoding='utf-8') as linhas:
        for x in linhas:
            agendamentos.append(json.loads(x.strip()))
    
    data = str(context.args[0])
    formato_hora = "%H:%M"
    selecionados = [x for x in agendamentos if x['data'] == data];
    por_horario = sorted(selecionados, key=lambda x: datetime.strptime(x['hora'], "%H:%M"))
    await update.message.reply_text("Seus Agendamentos:\n")
    for x in por_horario:
        await update.message.reply_text(f"{x['data']},  {x['hora']}, {x['duracao']}")
       
            
       
async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    agendamentos = []
    arquivo = Path('agendamentos.txt')
    if not arquivo.exists():
        await update.message.reply_text("Não há nenhum agendamento registrado.")
        return   
    
    with open("agendamentos.txt", "r",encoding='utf-8') as linhas:
        for x in linhas:
            agendamentos.append(json.loads(x.strip()))

    data = str(context.args[0])
    hora = str(context.args[1])
    sem_cancelados = [a for a in agendamentos if not (a["data"] == data and a["hora"] == hora)]
    
    with open("agendamentos.txt", "w", encoding="utf-8") as file:
        for agendamento in sem_cancelados:
            file.write(json.dumps(agendamento) + "\n") 
    await update.message.reply_text(f"Agendamento de {data} às {hora} cancelado com sucesso! ✅")    

def main():

    app = ApplicationBuilder().token("7919020982:AAGYNoGmvsk6aCOtyFqYUBkNz-TZBkVUbbc").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("agendar", agendar))
    app.add_handler(CommandHandler("consultar", consultar))
    app.add_handler(CommandHandler("cancelar", cancelar))
    app.run_polling()
if __name__ == "__main__":
    main()