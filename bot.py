import os
import requests
import telebot
import json
import time
from datetime import datetime
import pytz
import threading
from telebot import types # বাটন তৈরির জন্য নতুন ইম্পোর্ট করা হলো

# ══════════════════════════════════════════════════════════
# 🔧 Configuration
# ══════════════════════════════════════════════════════════
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = -1003801436002
LIVEACCESS_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tness/@public/api/liveaccess"

HEADERS = {
    "mauthapi": "MINQWI3C03A",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# ══════════════════════════════════════════════════════════
# 🌍 Country Flags Dictionary
# ══════════════════════════════════════════════════════════
COUNTRY_FLAGS = {
    "93":"🇦🇫", "355":"🇦🇱", "213":"🇩🇿", "1684":"🇦🇸", "376":"🇦🇩",
    "244":"🇦🇴", "1264":"🇦🇮", "1268":"🇦🇬", "54":"🇦🇷", "374":"🇦🇲",
    "297":"🇦🇼", "61":"🇦🇺", "43":"🇦🇹", "994":"🇦🇿", "971":"🇦🇪",
    "1242":"🇧🇸", "973":"🇧🇭", "880":"🇧🇩", "1246":"🇧🇧", "375":"🇧🇾",
    "32":"🇧🇪", "501":"🇧🇿", "229":"🇧🇯", "1441":"🇧🇲", "975":"🇧🇹",
    "591":"🇧🇴", "387":"🇧🇦", "267":"🇧🇼", "55":"🇧🇷", "246":"🇮🇴",
    "673":"🇧🇳", "359":"🇧🇬", "226":"🇧🇫", "257":"🇧🇮", "238":"🇨🇻",
    "855":"🇰🇭", "237":"🇨🇲", "1":"🇺🇸", "236":"🇨🇫", "235":"🇹🇩",
    "56":"🇨🇱", "86":"🇨🇳", "57":"🇨🇴", "269":"🇰🇲", "242":"🇨🇬",
    "243":"🇨🇩", "682":"🇨🇰", "506":"🇨🇷", "225":"🇨🇮", "385":"🇭🇷",
    "53":"🇨🇺", "599":"🇧🇶", "357":"🇨🇾", "420":"🇨🇿", "45":"🇩🇰",
    "253":"🇩🇯", "1767":"🇩🇲", "1809":"🇩🇴", "593":"🇪🇨", "20":"🇪🇬",
    "503":"🇸🇻", "240":"🇬🇶", "291":"🇪🇷", "372":"🇪🇪", "268":"🇸🇿",
    "251":"🇪🇹", "500":"🇫🇰", "298":"🇫🇴", "679":"🇫🇯", "358":"🇫🇮",
    "33":"🇫🇷", "594":"🇬🇫", "689":"🇵🇫", "241":"🇬🇦", "220":"🇬🇲",
    "995":"🇬🇪", "49":"🇩🇪", "233":"🇬🇭", "350":"🇬🇮", "30":"🇬🇷",
    "299":"🇬🇱", "1473":"🇬🇩", "590":"🇬🇵", "1671":"🇬🇺", "502":"🇬🇹",
    "224":"🇬🇳", "245":"🇬🇼", "592":"🇬🇾", "509":"🇭🇹", "504":"🇭🇳",
    "852":"🇭🇰", "36":"🇭🇺", "354":"🇮🇸", "91":"🇮🇳", "62":"🇮🇩",
    "98":"🇮🇷", "964":"🇮🇶", "353":"🇮🇪", "972":"🇮🇱", "39":"🇮🇹",
    "1876":"🇯🇲", "81":"🇯🇵", "962":"🇯🇴", "7":"🇷🇺", "254":"🇰🇪",
    "686":"🇰🇮", "850":"🇰🇵", "82":"🇰🇷", "965":"🇰🇼", "996":"🇰🇬",
    "856":"🇱🇦", "371":"🇱🇻", "961":"🇱🇧", "266":"🇱🇸", "231":"🇱🇷",
    "218":"🇱🇾", "423":"🇱🇮", "370":"🇱🇹", "352":"🇱🇺", "853":"🇲🇴",
    "389":"🇲🇰", "261":"🇲🇬", "265":"🇲🇼", "60":"🇲🇾", "960":"🇲🇻",
    "223":"🇲🇱", "356":"🇲🇹", "692":"🇲🇭", "596":"🇲🇶", "222":"🇲🇷",
    "230":"🇲🇺", "262":"🇷🇪", "52":"🇲🇽", "691":"🇫🇲", "373":"🇲🇩",
    "377":"🇲🇨", "976":"🇲🇳", "382":"🇲🇪", "212":"🇲🇦", "258":"🇲🇿",
    "95":"🇲🇲", "264":"🇳🇦", "674":"🇳🇷", "977":"🇳🇵", "31":"🇳🇱",
    "687":"🇳🇨", "64":"🇳🇿", "505":"🇳🇮", "227":"🇳🇪", "234":"🇳🇬",
    "683":"🇳🇺", "47":"🇳🇴", "968":"🇴🇲", "92":"🇵🇰", "680":"🇵🇼",
    "970":"🇵🇸", "507":"🇵🇦", "675":"🇵🇬", "595":"🇵🇾", "51":"🇵🇪",
    "63":"🇵🇭", "48":"🇵🇱", "351":"🇵🇹", "1787":"🇵🇷", "1939":"🇵🇷",
    "974":"🇶🇦", "40":"🇷🇴", "250":"🇷🇼", "590":"🇧🇱", "290":"🇸🇭",
    "1869":"🇰🇳", "1758":"🇱🇨", "508":"🇵🇲", "1784":"🇻🇨", "685":"🇼🇸",
    "378":"🇸🇲", "239":"🇸🇹", "966":"🇸🇦", "221":"🇸🇳", "381":"🇷🇸",
    "248":"🇸🇨", "232":"🇸🇱", "65":"🇸🇬", "1721":"🇸🇽", "421":"🇸🇰",
    "386":"🇸🇮", "677":"🇸🇧", "252":"🇸🇴", "27":"🇿🇦", "211":"🇸🇸",
    "34":"🇪🇸", "94":"🇱🇰", "249":"🇸🇩", "597":"🇸🇷", "46":"🇸🇪",
    "41":"🇨🇭", "963":"🇸🇾", "886":"🇹🇼", "992":"🇹🇯", "255":"🇹🇿",
    "66":"🇹🇭", "670":"🇹🇱", "228":"🇹🇬", "690":"🇹🇰", "676":"🇹🇴",
    "1868":"🇹🇹", "216":"🇹🇳", "90":"🇹🇷", "993":"🇹🇲", "1649":"🇹🇨",
    "688":"🇹翻", "256":"🇺🇬", "380":"🇺🇦", "44":"🇬🇧", "598":"🇺🇾",
    "998":"🇺🇿", "678":"🇻🇺", "379":"🇻🇦", "58":"🇻🇪", "84":"🇻🇳",
    "1284":"🇻🇬", "1340":"🇻🇮", "681":"🇼🇫", "967":"🇾🇪", "260":"🇿🇲",
    "263":"🇿🇼"
}

def get_country_flag(phone_number):
    """নাম্বার থেকে দেশ কোড খুঁজে বের করে ফ্ল্যাগ রিটার্ন করে"""
    for i in [4, 3, 2, 1]:
        code = phone_number[:i]
        if code in COUNTRY_FLAGS:
            return COUNTRY_FLAGS[code]
    return "🌍"

# ══════════════════════════════════════════════════════════
# 🔄 Monitoring Function
# ══════════════════════════════════════════════════════════
last_sent_time = None
last_response_hash = None

def monitor_liveaccess():
    """Liveaccess API monitoring"""
    global last_sent_time, last_response_hash
    
    print("✅ Bot চালু হয়েছে! পর্যবেক্ষণ শুরু করা হচ্ছে...")
    
    while True:
        try:
            response = requests.get(LIVEACCESS_URL, headers=HEADERS, timeout=5)
            
            if response.status_code == 200:
                json_data = response.json()
                
                if json_data.get("meta", {}).get("code") == 200:
                    services = json_data.get("data", {}).get("services", [])
                    current_time = time.time()
                    
                    # Hash তৈরি করো
                    current_hash = hash(json.dumps(json_data, sort_keys=True))
                    
                    # Logic: 60 সেকেন্ডের মধ্যে একই data = skip, নতুন = পাঠাও
                    should_send = False
                    
                    if last_sent_time is None:
                        should_send = True
                    elif (current_time - last_sent_time) >= 60:
                        should_send = True
                    elif current_hash != last_response_hash:
                        should_send = True
                    
                    if should_send:
                        print(f"✅ নতুন data! পাঠাচ্ছি... [{len(services)} services]")
                        
                        # প্রতিটি service
                        for service in services:
                            try:
                                sid = service.get("sid", "Unknown")
                                ranges = service.get("ranges", [])
                                last_at = service.get("last_at", 0)
                                
                                # Time format
                                try:
                                    bd_tz = pytz.timezone('Asia/Dhaka')
                                    dt = datetime.fromtimestamp(last_at/1000, tz=pytz.utc).astimezone(bd_tz)
                                    formatted_time = dt.strftime("%H:%M:%S")
                                except:
                                    formatted_time = "N/A"
                                
                                # 🎯 আপনার কাঙ্ক্ষিত ফরম্যাট অনুযায়ী মেসেজ তৈরি
                                message = f"🧩 <b>{sid.upper()}</b>\n"
                                message += "━━━━━━━━━━━━━━━━━\n"
                                
                                for range_id in ranges[:10]:
                                    flag = get_country_flag(range_id)
                                    # ক্লিক-টু-কপি কোড ফরম্যাটে রেঞ্জ সাজানো হলো
                                    message += f"└─ {flag} <code>{range_id}</code>\n"
                                
                                # 🛠️ ইনলাইন বাটন বা লিঙ্ক তৈরির লজিক (বাটন লিঙ্কের ইউআরএল গুলো আপনার সুবিধা মতো পরিবর্তন করে নেবেন)
                                markup = types.InlineKeyboardMarkup()
                                btn1 = types.InlineKeyboardButton("🔗 NUMBER BOT", url="https://t.me/SMSTOSMSBOT?start=start")
                                btn2 = types.InlineKeyboardButton("📊 MAIN CHANNEL", url="https://t.me/+LZrutZRrpbRkNDVl")
                                markup.row(btn1, btn2)
                                
                                # বাটন সহ মেসেজ পাঠানো হচ্ছে
                                bot.send_message(CHAT_ID, message, reply_markup=markup)
                                print(f"   ✅ {sid} পাঠানো হয়েছে")
                                
                            except Exception as e:
                                print(f"   ⚠️ Error: {e}")
                            
                            time.sleep(1)
                        
                        # Save
                        last_sent_time = current_time
                        last_response_hash = current_hash
                else:
                    print(f"⚠️ API Error: {json_data.get('meta', {}).get('code')}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(5)

# ══════════════════════════════════════════════════════════
# 🌐 Keep-Alive Server (Render-এ পোর্ট খোলা রাখার জন্য)
# ══════════════════════════════════════════════════════════
def run_keep_alive_server():
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class PingHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is alive")

        def do_HEAD(self):
            self.send_response(200)
            self.end_headers()

        def log_message(self, format, *args):
            pass

    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), PingHandler)
    server.serve_forever()


# ══════════════════════════════════════════════════════════
# 🚀 Start Bot
# ══════════════════════════════════════════════════════════
if __name__ == "__main__":
    # Render-এর জন্য keep-alive সার্ভার
    threading.Thread(target=run_keep_alive_server, daemon=True).start()

    # Background thread এ monitoring শুরু করো
    monitor_thread = threading.Thread(target=monitor_liveaccess, daemon=True)
    monitor_thread.start()
    
    # Bot polling শুরু করো
    print("🤖 Telegram Bot polling শুরু হচ্ছে...")
    bot.infinity_polling()
