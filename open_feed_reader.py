import feedparser
from telegram import Bot
import os
import asyncio
from supabase import create_client, Client
from datetime import datetime, timedelta, timezone

# ========== Configuration ==========
TOKEN =  os.getenv('TELEGRAM_BOT_TOKEN')
RSS_FEED_URL = 'https://www.open.online/feed/'
CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
# ========== end Configuration ==========

bot = Bot(token=TOKEN)
tablename = 'posted_links'
conn: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

def check_old_links_and_delete():
    # Calcola la data di 2 giorni fa
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=2)

    # Esegui il DELETE dei record più vecchi di due giorni
    conn.table("posted_links")\
        .delete()\
        .lt("inserted_at", cutoff_date.isoformat())\
        .execute()

def get_feed_entries():
    feed = feedparser.parse(RSS_FEED_URL)
    return feed.entries

def link_is_posted(link):
    data = conn.table(tablename)\
        .select("*")\
        .eq("url", link)\
        .execute()
    return len(data.data) > 0

def save_link_to_db(link):
    conn.table(tablename)\
        .insert({"url": link})\
        .execute()

async def send_new_articles():
    for entry in get_feed_entries():
        if not link_is_posted(entry.link):
            text = f"📰 <b>{entry.title}</b>\n\n{entry.link}"
            try:
                await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode='HTML', disable_notification=True)
            except Exception as e:
                print(f"Errore Telegram: {e}")
            save_link_to_db(entry.link)

async def main():
    check_old_links_and_delete()
    await send_new_articles()

# Avvio dello script
if __name__ == '__main__':
    asyncio.run(main())