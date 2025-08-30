import os
import asyncio
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN

# Create Pyrogram bot client
app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Simple start command
@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text("👋 Hello! Bot is running fine.")

# Example echo
@app.on_message(filters.text & ~filters.command("start"))
async def echo(client, message):
    await message.reply_text(f"You said: {message.text}")

if __name__ == "__main__":
    app.run()
