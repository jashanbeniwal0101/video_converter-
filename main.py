# main.py
import os
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN

# Initialize Pyrogram client
app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50,  # allow multiple tasks
    in_memory=True
)

# /start command
@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(
        "👋 Hello! Bot is running fine.\n\n"
        "📥 Send me any video, audio, document, or zip file and I’ll handle it."
    )

# Echo for text (optional)
@app.on_message(filters.text & ~filters.command("start"))
async def echo(client, message):
    await message.reply_text(f"📝 You said: {message.text}")

# Handle media uploads
@app.on_message(filters.video | filters.audio | filters.document)
async def handle_media(client, message):
    file = message.document or message.video or message.audio
    if not file:
        return await message.reply_text("❌ Unsupported file.")
    
    file_name = file.file_name if hasattr(file, "file_name") else "unknown"
    file_size = round(file.file_size / (1024 * 1024), 2)

    await message.reply_text(
        f"✅ File received!\n\n"
        f"📂 **Name:** {file_name}\n"
        f"📦 **Size:** {file_size} MB\n"
        f"⚙️ Stored successfully."
    )

if __name__ == "__main__":
    print("🚀 Bot starting...")
    app.run()
