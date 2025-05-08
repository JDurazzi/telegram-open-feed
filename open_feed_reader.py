import feedparser
from telegram import Bot
import os
import time
import asyncio
import sqlite3

# ========== Configuration ==========
TOKEN =  os.getenv('TELEGRAM_BOT_TOKEN')
RSS_FEED_URL = 'https://www.open.online/feed/'
CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
# ========== end Configuration ==========

bot = Bot(token=TOKEN)
file_path = 'posted_links.db'
posted_links = set()

def init_db():
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def get_creation_time(file_path):
    # Ottieni la data di creazione del file
    return os.path.getctime(file_path)

def check_db_age_and_init():
    # Controlla se il file esiste e se è più vecchio di 24 ore
    if os.path.exists(file_path):
        creation_time = get_creation_time(file_path)
        current_time = time.time()
        if (current_time - creation_time) > 172.800:  # 172.800 secondi in due giorni
            os.remove(file_path)
            init_db()
    else:
        init_db()

def get_feed_entries():
    feed = feedparser.parse(RSS_FEED_URL)
    return feed.entries

def link_is_posted(link):
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM links WHERE link = ?', (link,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def save_link_to_db(link):
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO links (link) VALUES (?)', (link,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Ignora se il link è già presente
    finally:
        conn.close()

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
    check_db_age_and_init()
    await send_new_articles()

# Avvio dello script
if __name__ == '__main__':
    main()