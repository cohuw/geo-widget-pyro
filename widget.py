import asyncio
import aiohttp
import pytz
from pyrogram import Client, enums
from datetime import datetime

# --- CONFIG ---
API_ID = 0 # ПОСТАВЬ СВОЙ API ID
API_HASH = "0" # ПОСТАВЬ СВОЙ API HASH
BOT_TOKEN = "" # ПОСТАВЬ СВОЙ BOT TOKEN
CHAT_ID = -1000000000000 # ПОСТАВЬ СВОЙ CHAT ID
LOG_MESSAGE_ID = 0 # ПОСТАВЬ СВОЙ LOG MESSAGE ID

CITIES = {
    "Tokyo":    {"tz": "Asia/Tokyo",        "lat": 35.6895, "lon": 139.6917},
    "Seoul":    {"tz": "Asia/Seoul",        "lat": 37.5665, "lon": 126.9780},
    "Almaty":   {"tz": "Asia/Almaty",       "lat": 43.2220, "lon": 76.8512},
    "Astana":   {"tz": "Asia/Almaty",       "lat": 51.1605, "lon": 71.4277},
    "Dubai":    {"tz": "Asia/Dubai",        "lat": 25.2048, "lon": 55.2708},
    "Moscow":   {"tz": "Europe/Moscow",     "lat": 55.7558, "lon": 37.6173},
    "Kyiv":     {"tz": "Europe/Kyiv",       "lat": 50.4501, "lon": 30.5234},
    "Berlin":   {"tz": "Europe/Berlin",     "lat": 52.5200, "lon": 13.4050},
    "London":   {"tz": "Europe/London",     "lat": 51.5074, "lon": -0.1278},
    "New York": {"tz": "America/New_York",  "lat": 40.7128, "lon": -74.0060},
    "S-Fran":   {"tz": "America/Los_Angeles","lat": 37.7749, "lon": -122.4194}
}

def get_solar_icon(hour):
    if 0 <= hour < 5: return "✨" # ГЛУБОКАЯ НОЧЬ
    if 5 <= hour < 9: return "🌅" # УТРО/РАССВЕТ
    if 9 <= hour < 17: return "☀️" # ДЕНЬ
    if 17 <= hour < 21: return "🌇" # ВЕЧЕР/ЗАКАТ
    return "🌙" 

async def get_weather(session, lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    wmo_codes = {
        0: "☀️", 1: "🌤", 2: "⛅️", 3: "☁️", 45: "🌫", 48: "❄️", 
        51: "🌧", 61: "🌦", 63: "🌧", 65: "⛈", 71: "❄️", 95: "⚡️"
    }
    try:
        async with session.get(url, timeout=5) as response:
            if response.status == 200:
                data = await response.json()
                curr = data['current_weather']
                return f"{round(curr['temperature'])}°C {wmo_codes.get(curr['weathercode'], '🛰')}"
            return "ERR"
    except:
        return "OFF"

async def run_logger(app):
    async with aiohttp.ClientSession() as session:
        while True:
            base_hour = datetime.now(pytz.timezone("Asia/Almaty")).hour
            pulse = get_solar_icon(base_hour)
            
            log_content = f"<code>┏━━━━━ Mini Widget | TIME ICON {pulse}</code>\n"
            
            city_names = list(CITIES.keys())
            tasks = [get_weather(session, CITIES[n]['lat'], CITIES[n]['lon']) for n in city_names]
            results = await asyncio.gather(*tasks)

            for i, name in enumerate(city_names):
                tz = pytz.timezone(CITIES[name]['tz'])
                time_str = datetime.now(tz).strftime("%H:%M")
                weather = results[i]
                
                log_content += f"<code>┣</code> <b>{name:<9}:</b> <code>{time_str}</code> | <i>{weather}</i>\n"
            
            log_content += f"<code>┗━━━━━━━━━━━━━━━━━━━━━━</code>\n"
            
            try:
                await app.edit_message_text(CHAT_ID, LOG_MESSAGE_ID, log_content, parse_mode=enums.ParseMode.HTML)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Heartbeat: {pulse}")
            except Exception as e:
                print(f"Update failed: {e}")

            await asyncio.sleep(900)

async def main():
    app = Client("widget", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    async with app:
        await run_logger(app)

if __name__ == "__main__":
    asyncio.run(main())