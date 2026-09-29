# 📰 OpenFeedReaderBot [![Run Feed Reader](https://github.com/JDurazzi/telegram-open-feed/actions/workflows/run-bot.yml/badge.svg?event=workflow_run)](https://github.com/JDurazzi/telegram-open-feed/actions/workflows/run-bot.yml)

OpenFeedReaderBot è uno script Python che legge automaticamente gli articoli pubblicati nel feed RSS di [Open.online](https://www.open.online/feed/) e li pubblica in un canale Telegram.

---

## 📌 Funzionalità

- Estrae gli articoli dal feed RSS di Open.
- Invia automaticamente i nuovi articoli a un canale Telegram.
- Evita messaggi duplicati grazie a un controllo sui link già inviati.
- Supporta HTML per un formato messaggio più leggibile.
- Utilizza `asyncio` per una gestione asincrona moderna.

---

## ⚙️ Requisiti

- Python 3.8 o superiore
- Un bot Telegram con token valido
- Il bot deve essere aggiunto come amministratore nel canale Telegram in cui pubblicherà

---

## 🛠 Installazione

Clona la repository ed entra nella cartella:

```bash
git clone https://github.com/tuo-username/OpenFeedReaderBot.git
cd OpenFeedReaderBot
```

Crea e attiva un ambiente virtuale (consigliato):

```bash
python3 -m venv venv
source venv/bin/activate
```

Installa le dipendenze:

```bash
pip install python-telegram-bot feedparser
```

---

## 🔐 Configurazione

Imposta le seguenti variabili d'ambiente nel terminale o nel tuo `.env`:

```bash
export TELEGRAM_BOT_TOKEN="il_tuo_token_telegram"
export TELEGRAM_CHANNEL_ID="-100xxxxxxxxxx"
```

> 🔹 L'ID del canale deve iniziare con `-100`.  
> 🔹 Il tuo bot deve essere amministratore del canale con permessi per inviare messaggi.

---

## ▶️ Esecuzione

Avvia lo script:

```bash
python open_feed_reader.py
```

Lo script effettua una singola lettura del feed. Per monitorare il feed periodicamente, puoi:

1. Decommentare la riga `await asyncio.sleep(600)` e inserirla in un ciclo `while True:`.
2. Oppure schedulare lo script con `cron` o altri strumenti.

---

## 📄 Esempio di output nel canale Telegram

```
📰 <Titolo dell'articolo>

https://www.open.online/2025/05/08/esempio-articolo/
```

Il messaggio viene inviato in formato HTML e con notifica silenziata.

---

## 📁 File principali

- `open_feed_reader.py`: Script principale da eseguire.
- `README.md`: Questo file.

---
 
