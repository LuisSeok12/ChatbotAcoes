import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from chat import run_round
from finance_utils import get_stock_price

load_dotenv()

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

welcome = ("Olá! Sou um bot de cotações.\n"
    "Exemplos: 'quanto está AAPL?', 'preço da PETR4', 'variação de LIGT3 no último ano'.\n")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(welcome)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(welcome)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = (update.message.text or "").strip()
    if not user_text:
        return
    try:
        resp = run_round(user_text, get_stock_price)
        await update.message.reply_text(resp or "Não conseguir formular a resposta no momento")
    except Exception as e:
        await update.message.reply_text(f"Erro ao processar a solicitação: {e}")

def main():
    if not bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN não encontrado no .env")
    
    app = Application.builder().token(bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot rodando, aperte CRTL C para sair")
    app.run_polling(close_loop=False)

if __name__ == "__main__":

    main()
