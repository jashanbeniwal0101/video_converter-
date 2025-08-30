# Very simple bulk queue: user can forward/add several messages and then call /bulk_run action
from pyrogram import Client, filters
from pyrogram.types import Message
from collections import defaultdict

bulk_store = defaultdict(list)  # chat_id -> list of message objects (ids)


def init(app: Client):
    @app.on_message(filters.command('bulk_add'))
    async def bulk_add(_, m: Message):
        if not m.reply_to_message: return await m.reply_text('Reply to a message to add it to bulk set')
        bulk_store[m.chat.id].append(m.reply_to_message.message_id)
        await m.reply_text(f'Added message {m.reply_to_message.message_id} to bulk set ({len(bulk_store[m.chat.id])} items)')

    @app.on_message(filters.command('bulk_list'))
    async def bulk_list(_, m: Message):
        items = bulk_store.get(m.chat.id, [])
        await m.reply_text(f'Bulk items: {items}')

    @app.on_message(filters.command('bulk_clear'))
    async def bulk_clear(_, m: Message):
        bulk_store.pop(m.chat.id, None)
        await m.reply_text('Cleared bulk set')

    @app.on_message(filters.command('bulk_run'))
    async def bulk_run(_, m: Message):
        parts = (m.text or '').split()
        if len(parts) < 2:
            return await m.reply_text('Usage: /bulk_run convert|zip|remove_audio')
        action = parts[1]
        items = bulk_store.get(m.chat.id, [])
        if not items:
            return await m.reply_text('No items in bulk set')
        await m.reply_text(f'Running {action} on {len(items)} items...')
        # naive implementation: iterate and forward to the bot handlers (not implemented fully here)
        for mid in items:
            await m.reply_text(f'Would process message id {mid} with {action}')
        await m.reply_text('Bulk run complete (simulation)')
