from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

files_db = []

async def save_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg.document:
        files_db.append({
            "name": msg.document.file_name,
            "file_id": msg.document.file_id
        })
        await msg.reply_text(f"Saved: {msg.document.file_name}")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args).lower()
    results = [f for f in files_db if query in f["name"].lower()]

    if results:
        for file in results:
            await update.message.reply_document(file["file_id"])
    else:
        await update.message.reply_text("No files found")

app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

app.add_handler(MessageHandler(filters.Document.ALL, save_file))
app.add_handler(CommandHandler("search", search))

app.run_polling()