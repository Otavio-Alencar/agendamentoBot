from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pathlib import Path
import json
from datetime import datetime
from datetime import time
import random
import os
from dotenv import load_dotenv

load_dotenv()
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem = f"""
    Olá eu sou o {os.getenv('BOT_NAME')}, seja bem vindo!

    Aqui está a lista de comandos para você utilizar:
    ➤ /start - Mostra os comandos
    ➤ /hello - Retorna um olá mundo
    ➤ /agendar  *data *hora *duração - Adiciona um agendamento
    ➤ /consultar  *data - Mostra os seus agendamentos
    ➤ /cancelar  *data *hora - Cancela um agendamento existente
    ➤ /sugerir  *data *duração - Sugere um agendamento

"""
    await update.message.reply_text(mensagem)

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
    if len(sem_cancelados)  == len(agendamentos):
         await update.message.reply_text(f"Não encontramos o agendamento indicado, verifique se a data e horário estão corretos") 
         return
    with open("agendamentos.txt", "w", encoding="utf-8") as file:
        for agendamento in sem_cancelados:
            file.write(json.dumps(agendamento) + "\n") 
    await update.message.reply_text(f"Agendamento de {data} às {hora} cancelado com sucesso!")    


async def sugerir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    agendamentos = []
    arquivo = Path('agendamentos.txt')
    if not arquivo.exists():
        f = open("agendamentos.txt", "x")
    
    with open("agendamentos.txt", "r",encoding='utf-8') as linhas:
        for x in linhas:
            agendamentos.append(json.loads(x.strip()))
    data = str(context.args[0])
    duracao = str(context.args[1])
    hora =  '00:00'
 
    while True:
        hora =  time(random.randint(7,18),random.randint(0,59)).strftime("%H:%M")
        lista  = [x for x in agendamentos if hora == x['hora']]
        if len(lista) > 0:
            continue
        else:
            break
    await update.message.reply_text(f"Você pode agendar em {data}, às {hora}, com duração de {duracao} minutos") 
    

def main():

    app = ApplicationBuilder().token(os.getenv('MY_SECRET_TOKEN')).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("agendar", agendar))
    app.add_handler(CommandHandler("consultar", consultar))
    app.add_handler(CommandHandler("cancelar", cancelar))
    app.add_handler(CommandHandler("sugerir", sugerir))
    app.run_polling()
if __name__ == "__main__":
    main()