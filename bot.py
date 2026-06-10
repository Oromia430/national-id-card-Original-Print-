import os
import telebot
import cv2
import numpy as np
from PIL import Image
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔑 CONFIGURATION
TOKEN = '8974775722:AAEdkBUxx02cwzLLzGT6Fa5hqSWtveqGz6A'
ADMIN_ID = 123456789  # Chat ID kee (Elias) as keessa kaa'i

bot = telebot.TeleBot(TOKEN)

# DATABASE YEROO GABAABAA (Memory Storage)
USER_STATES = {}   
USER_IMAGES = {}   
PAID_USERS = {}    

# 🏦 LIST LAKKOOFSOTA KAFALTII SIRRII TA'AN
# Akkaata kaffaltiin siif seenun as keessatti itti dabalamaa deema
VALID_TRANSACTIONS = [
    "FT26162HX8P3", 
    "FT26163MZ9K4", 
    "TXN98765432"
]

# --- HOJII GADI FAGEENYAA: ADVANCED COMPUTER VISION (CV2) ---

def enhance_and_crop_id(image_path):
    """
    Fakkii screenshot keessaa kaardicha addaan baasa, jallina isaa qajeelcha,
    akkasumas qulqullina qubeewwanii (FAN, Maqaa) gadi fageenyaan dabala.
    """
    # 1. Fakkii dubbisuu
    img = cv2.imread(image_path)
    if img is None:
        return None
        
    h_orig, w_orig, _ = img.shape
    
    # 2. IMAGE ENHANCEMENT (Qulqullina Guddisuu)
    # Gara Gray-tti jijjiiruu, itti aansee noise balleessuu
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Adaptive Thresholding fayyadamanii qubeewwan qulqulleessuu
    edged = cv2.Canny(blur, 40, 130)
    
    # 3. AUTOMATIC CONTOUR DETECTION (Kofoota Kaardichaa Barbaaduu)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cropped = None
    if contours:
        # Contour isa naannoo bal'aa qabu qofa fudhachuu
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            
            # Kofoota 4 yoo argate (Bifa Kaardichaa)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                if w > w_orig * 0.4 and h > h_orig * 0.4:
                    cropped = img[y:y+h, x:x+w]
                    break
                    
        if cropped is None:
            # Yoo kofoota 4 argachuu baate, rectangle kaardichaa idilee fudhata
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            if w > w_orig * 0.4 and h > h_orig * 0.4:
                cropped = img[y:y+h, x:x+w]

    # 4. FALLBACK STRATEGY (Yoo OpenCV'n muruu dadhabe)
    if cropped is None:
        # Iskiriinshotii gidduudhaa %75 mura (Buttons gubbaa fi jalaa hambisa)
        start_x = int(w_orig * 0.07)
        start_y = int(h_orig * 0.14)
        end_x = int(w_orig * 0.93)
        end_y = int(h_orig * 0.82)
        cropped = img[start_y:end_y, start_x:end_x]

    # 5. SHARPNESS & CONTRAST (Qulqullina Qubeewwanii fiduu)
    # Filtari kanaan qubeewwan akka dammaqan godhama
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    enhanced = cv2.filter2D(cropped, -1, kernel)
    
    return enhanced


def create_final_id_pdf_or_image(front_path, back_path, output_path):
    """Kaardii lamaan qulqullina CR-80 standardiin dizaayinii tokko godhee maku"""
    # Gadi fageenyaan fakkii qulqulleessanii muruu
    front_cv = enhance_and_crop_id(front_path)
    back_cv = enhance_and_crop_id(back_path)
    
    # OpenCV irraa gara Pillow Image-itti geeddaruu
    front_pil = Image.fromarray(cv2.cvtColor(front_cv, cv2.COLOR_BGR2RGB))
    back_pil = Image.fromarray(cv2.cvtColor(back_cv, cv2.COLOR_BGR2RGB))
    
    # STANDARD CR-80 PVC SIZE (Super resolution $1011 \times 638$)
    card_w, card_h = 1011, 638
    front_final = front_pil.resize((card_w, card_h), Image.Resampling.LANCZOS)
    back_final = back_pil.resize((card_w, card_h), Image.Resampling.LANCZOS)
    
    # CANVAS ADII QOPHEESSUU
    margin_x = 60  
    margin_y = 90  
    
    canvas_w = (card_w * 2) + (margin_x * 3)
    canvas_h = card_h + (margin_y * 2)
    canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    
    # Fakkiiwwan walbira kaa'uu
    canvas.paste(front_final, (margin_x, margin_y))
    canvas.paste(back_final, (card_w + (margin_x * 2), margin_y))
    
    # Maayyii irratti qulqullina 100% eeganii kuusuu (Print-fii)
    canvas.save(output_path, "JPEG", quality=100, subsampling=0)


# --- TELEGRAM BOT HANDLERS ---

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    USER_STATES[user_id] = None
    USER_IMAGES[user_id] = {}
    
    text = (f"Akkam {message.from_user.first_name}!\n\n"
            f"Bot kun screenshot Fayda ID keetii gara bifa original print ta'uutti siif jijjiira.\n"
            f"Tajaajila kana fayyadamuuf kaffaltii Birrii 50 raawwachuu qabdu.\n\n"
            f"🏦 *Odeeffannoo Kaffaltii:* \n"
            f"📌 *CBE Baankii:* `1000270143788`\n"
            f"👤 *Maqaa:* Elias Fikadu Mulata\n"
            f"📌 *Telebirr:* `0913701367`\n\n"
            f"Erga kaffaltanii booda 'Kaffaltii Mirkaneessi' kan jedhu cuqaasaa.")
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ Kaffaltii Mirkaneessi", callback_data="verify_tx"))
    bot.send_message(user_id, text, reply_markup=markup, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == "verify_tx")
def handle_callbacks(call):
    user_id = call.from_user.id
    USER_STATES[user_id] = 'Eegaa_Transaction_Number'
    bot.send_message(user_id, "✍️ Maaloo lakkoofsa daddabarsaa kaffaltii keetii (**Transaction ID / Ref Number**) guutummaatti asirratti barreessii ergi.\n\nFakkeenya: `FT26162HX8P3` ykn `TXN98765432`")


@bot.message_handler(func=lambda message: USER_STATES.get(message.from_user.id) == 'Eegaa_Transaction_Number')
def verify_transaction_number(message):
    user_id = message.from_user.id
    input_tx = message.text.strip()
    
    # Auto-Verification Logic
    if input_tx in VALID_TRANSACTIONS:
        PAID_USERS[user_id] = True
        USER_STATES[user_id] = 'Eegaa_Fuulduraa'
        
        # Tikkeetti sana list keessaa balleessuu (irra deebii ittisuuf)
        VALID_TRANSACTIONS.remove(input_tx)
        
        bot.reply_to(message, "🎉 Kaffaltiin keessan of-caalaatti mirkanaa'eera! Hojii keenya ni jalqabna.\n\n👉 Maaloo fakkii ID keetii kan *GARA FUULDURAA* (Front) ergi.")
        bot.send_message(ADMIN_ID, f"🔔 [AUTO-APPROVED]: User {user_id} lakkoofsa `{input_tx}` tajaajila baneera.")
    else:
        bot.reply_to(message, "❌ Lakkoofsi daddabarsaa ati ergite sirrii miti ykn kaffaltiin sun hin argamne.\n\nMaaloo lakkoofsicha sirreessitee yaali ykn Admin qunnami.")


@bot.message_handler(content_types=['photo'])
def handle_id_photos(message):
    user_id = message.from_user.id
    state = USER_STATES.get(user_id)
    
    if user_id not in PAID_USERS:
        bot.reply_to(message, "⚠️ Maaloo tajaajila argachuuf dura kaffaltii raawwadhaa. /start tuqaa.")
        return
        
    if state == 'Eegaa_Fuulduraa':
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)
        front_path = f"raw_front_{user_id}.jpg"
        with open(front_path, 'wb') as f:
            f.write(downloaded)
            
        USER_IMAGES[user_id]['front'] = front_path
        USER_STATES[user_id] = 'Eegaa_Duubaa'
        bot.reply_to(message, "📸 Gara fuulduraa fudhadheera! Amma immoo fakkii ID keetii kan *GARA DUUBAA* (Back) ergi.")
        
    elif state == 'Eegaa_Duubaa':
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)
        back_path = f"raw_back_{user_id}.jpg"
        with open(back_path, 'wb') as f:
            f.write(downloaded)
            
        USER_IMAGES[user_id]['back'] = back_path
        bot.reply_to(message, "⏳ Nu eegi, OpenCV fi Pillow fayyadamnee fakkicha qulqulleessinee template bogaa qopheessaa jirra...")
        
        try:
            front = USER_IMAGES[user_id]['front']
            back = USER_IMAGES[user_id]['back']
            output_final = f"print_ready_{user_id}.jpg"
            
            # Hojii advanced template-ii raawwachuu
            create_final_id_pdf_or_image(front, back, output_final)
            
            # Fakkii qophaa'e deebisanii erguu
            with open(output_final, 'rb') as photo:
                bot.send_photo(user_id, photo, caption="🎉 Kunoo Fayda ID keessan bifa kanaan print-fii qophaa'eera! Gallatoomaa.")
                
            # Files irraa qulqulleessuu
            os.remove(front)
            os.remove(back)
            os.remove(output_final)
            
            USER_STATES[user_id] = None
            USER_IMAGES[user_id] = {}
            del PAID_USERS[user_id]
            
        except Exception as e:
            bot.reply_to(message, f"Dogoggora uumameera: {str(e)}")

print("Botiin kee gadi fageenyaan qophaa'ee jira...")
bot.infinity_polling()
