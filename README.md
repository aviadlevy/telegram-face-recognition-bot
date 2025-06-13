# 🤖 Face Recognition Telegram Bot (Local & Lightweight)

A privacy-first, offline face recognition system that runs on your own hardware and interacts via Telegram. Designed for mini PCs (1–2 CPU, 4GB RAM), this bot detects if your known faces (e.g., family members) appear in photos you send.

---

## ✨ Features

- **Local & Private:** All processing is done locally. No cloud, no data leaks.
- **Telegram Integration:** Send photos to your bot and get instant feedback.
- **Multiple Faces:** Supports recognition of multiple known people.
- **Batch Handling:** Handles multiple photos per message.
- **Reactions:** Bot reacts with 👀 while analyzing, ✅ for matches, ❌ for no match.
- **Easy Setup:** Docker & Docker Compose support, or run locally with [uv](https://github.com/astral-sh/uv).
- **Automatic Cleanup:** Periodically deletes old uploads to save space and protect privacy.

---

## 🚀 Quick Start

### 1. Prepare Known Face Images

Place clear, front-facing photos of each person you want to recognize in the `reference_photos/` folder:

```
reference_photos/
├── son1.jpg
├── daughter1.jpg
```

### 2. Generate Embeddings

Run the following to generate face embeddings:

```bash
python save_embedding.py
```
This will create `.pt` files in the `embeddings/` directory.

### 3. Configure Secrets

Create a `.env` file (not tracked by git) in your project root:

```
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here
```

You can also set cleanup options (in seconds):

```
CLEANUP_INTERVAL=3600    # How often to run cleanup (default: 1 hour)
CLEANUP_MAX_AGE=3600     # Delete files older than this (default: 1 hour)
```

### 4. Build and Run with Docker Compose

```bash
docker compose up --build
```

Or, to run locally with [uv](https://github.com/astral-sh/uv):

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
uv pip install -r requirements.txt
uv python bot.py
```

---

## 🤳 Using the Bot

1. Start a chat with your bot on Telegram.
2. Send one or more photos.
3. The bot will:
   - React with 👀 while analyzing each photo.
   - Reply with ✅ if any known face is detected.
   - Reply with ❌ if no match is found.

---

## 🧹 Scheduled Cleanup

The bot automatically cleans the `uploads/` directory to save disk space and protect your privacy.  
By default, it deletes files older than 1 hour every hour.

You can configure this in your `.env` or `docker-compose.yml`:

```yaml
environment:
  - CLEANUP_INTERVAL=1800    # Cleanup every 30 minutes
  - CLEANUP_MAX_AGE=7200     # Delete files older than 2 hours
```

---

## 🗂️ File Structure

```
project-root/
├── bot.py                # Telegram bot logic
├── recognizer.py         # Face recognition logic
├── save_embedding.py     # Tool to save known face embeddings
├── cleanup.py            # Scheduled cleanup logic
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements.lock.txt
├── .env                  # Secrets (not tracked by git)
├── reference_photos/     # Input photos of known faces
├── embeddings/           # Output face embeddings
├── uploads/              # Temporary folder for received photos
```

---

## 🧪 Requirements

- Python 3.12+
- facenet-pytorch
- python-telegram-bot >= 20.7
- torch
- torchvision
- pillow
- Docker (optional, for containerized runs)
- uv (optional, for fast local runs)

---

## 🔒 Security & Privacy

- **All processing is local.** No images or data leave your machine.
- **No open ports required.** Uses Telegram polling.
- **Automatic cleanup** of uploaded images.

---

## ➕ Adding More Faces

Just drop more images into `reference_photos/` and rerun:

```bash
python save_embedding.py
```

---

**Enjoy your private, local face recognition bot!**
