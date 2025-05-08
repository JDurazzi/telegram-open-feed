import feedparser
from telegram import Bot
import os
import time
import asyncio

# ========== Configuration ==========
TOKEN =  os.getenv('TELEGRAM_BOT_TOKEN')
RSS_FEED_URL = 'https://www.open.online/feed/'
CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
# ========== end Configuration ==========

bot = Bot(token=TOKEN)
posted_links = set()

def get_feed_entries():
    feed = feedparser.parse(RSS_FEED_URL)
    return feed.entries

async def send_new_articles():
    global posted_links
    for entry in get_feed_entries():
        if entry.link not in posted_links:
            text = f"📰 <b>{entry.title}</b>\n\n{entry.link}"
            try:
                await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode='HTML', disable_notification=True)
            except Exception as e:
                print(f"Errore Telegram: {e}")
            posted_links.add(entry.link)

async def main():
    await send_new_articles()
    await asyncio.sleep(600)  # Check every 10 minutes

# Avvio dello script
if __name__ == '__main__':
    asyncio.run(main())