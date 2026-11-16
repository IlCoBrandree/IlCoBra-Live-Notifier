import os
import json
import asyncio
import urllib.parse
import urllib.request
from pathlib import Path
from TikTokLive import TikTokLiveClient

USERNAME = "Il__CoBra"
STATE_FILE = Path("tiktok_state.json")

def send_telegram():
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    message = (
        "🔴 IL COBRA È LIVE SU TIKTOK! 🐍\n\n"
        "🔥 Ragazzi, siamo in diretta!\n"
        "🎮 Vi aspetto tutti in live!\n\n"
        "📱 https://www.tiktok.com/@Il__CoBra/live"
    )
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": message}).encode()
    with urllib.request.urlopen(url, data=data, timeout=20) as response:
        print("Notifica Telegram inviata:", response.status)

async def main():
    client = TikTokLiveClient(unique_id=f"@{USERNAME}")
    is_live = await client.is_live()
    previous = {}
    if STATE_FILE.exists():
        previous = json.loads(STATE_FILE.read_text())
    was_live = previous.get("live", False)
    print(f"TikTok live: {is_live}")
    print(f"Stato precedente: {was_live}")
    if is_live and not was_live:
        send_telegram()
    STATE_FILE.write_text(json.dumps({"live": is_live}))

if __name__ == "__main__":
    asyncio.run(main())
  
