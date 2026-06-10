import os
import telebot
import cv2
import numpy as np
from PIL import Image
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔑 CONFIGURATION
# Render irratti Environment Variables keessatti itti dabinna. 
# Yoo achi dides, Token kee sirriitti mallattoo ':' qabaachuu isaa mirkaneeffadhuu as keessa kaa'i.
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '7238260846:AAFlYgXpYl2gXvOz_VfP2M7wWhxEXAMPLE')  
ADMIN_ID = 123456789  # Chat ID kee (Elias) as keessa kaa'i lakkofsa qofa

bot = telebot.TeleBot(TOKEN)

# DATABASE YEROO GABAABAA
USER_STATES = {}   
USER_IMAGES = {}   
PAID_USERS = {}    

# --- HOJII IMAGE PROCESSING (CROP & ALIGN) ---

def auto_crop_id(image_path):
    """Fakkii screenshot keessaa kaardii Fayda ID qofa bifa sirriin addaan baasa"""
    img = cv2.imread(image_path)
    if img is None:
        return None
        
    h_orig, w_orig, _ = img.shape
    
    # Gubbaa fi jala irraa kofalchiftoota bilbilaa (buttons) muranii balleessuu
    start_x = int(w_orig * 0.05)
    start_y = int(h_orig * 0.14)
    end_x = int(w_orig * 0.95)
    end_y = int(h_orig * 0.84)
    
    cropped = img[start_y:end_y, start_x:end_x]
    
    # Qulqullina qubeewwanii dabaluu (Sharpening Filter)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    enhanced = cv2.filter2D(cropped, -1, kernel)
    return enhanced

def create_final_id_template(front_path, back_path, output_path):
    """Kaardii lamaan qulqullinaan CR-80 standardiin bifa sirriin walbira qaba"""
    front_cv = auto_crop_id(front_path)
    back_cv = auto_crop_id(back_path)
    
    # OpenCV to Pillow Image geeddaruu
    front_pil = Image.fromarray(cv2.cvtColor(front_cv, cv2.COLOR_BGR2RGB))
    back_pil = Image.fromarray(cv2.cvtColor(back_cv, cv2.COLOR_BGR2RGB))
    
    # Standard CR-80 Size ($1011 \times 638$ Pixels)
    card_w, card_h = 1011, 638
    front_final = front_pil.resize((card_w, card_h), Image.Resampling.LANCZOS)
    back_final = back_pil.resize((card_w, card_h), Image.Resampling.LANCZOS)
    
    # CANVAS ADII (White Background)
    margin_x = 60  
    margin_y = 90  
    
    canvas_w = (card_w * 2) + (margin_x * 3)
    canvas_h = card_h + (margin_y * 2)
    canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    
    # Fakkiiwwan bifa sirriin walbira kaa'uu (Kofni isaanii akka hin garagalleef)
    canvas.paste(front_final, (margin_x, margin_y))
    canvas.paste(back_final, (card_w + (margin_x * 2), margin_y))
    
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
    bot.send_message(user_id, "✍️ Maaloo lakkoofsa daddabarsaa kaffaltii keetii (**Transaction ID / Ref Number**) guutummaatti asirratti barreessii ergi.\n\nFakkeenya: `DFA0RZLEIA` ykn `FT26162HX8P3`")


@bot.message_handler(func=lambda message: USER_STATES.get(message.from_user.id) == 'Eegaa_Transaction_Number')
def verify_transaction_number(message):
    user_id = message.from_user.id
    input_tx = message.text.strip()
    
    # AUTOMATIC APPROVAL LOGIC (Jecha dheerina qubee 6 ol jiru kamiyyuu ni fudhata)
    if len(input_tx) >= 6:
        PAID_USERS[user_id] = True
        USER_STATES[user_id] = 'Eegaa_Fuulduraa'
        
        bot.reply_to(message, "🎉 Kaffaltiin keessan of-caalaatti mirkanaa'eera! Hojii keenya ni jalqabna.\n\n👉 Maaloo fakkii ID keetii kan *GARA FUULDURAA* (Front) ergi.")
        try:
            bot.send_message(ADMIN_ID, f"🔔 [AUTO-APPROVED]: User {user_id} lakkoofsa `{input_tx}` tajaajila baneera.")
        except Exception:
            pass
    else:
        bot.reply_to(message, "❌ Lakkoofsi daddabarsaa ati ergite sirrii miti. Maaloo lakkofsa sirrii galchi.")


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
        bot.reply_to(message, "⏳ Nu eegi, fakkicha qulqulleessinee dizaayinii isaa sirreessaa jirra...")
        
        try:
            front = USER_IMAGES[user_id]['front']
            back = USER_IMAGES[user_id]['back']
            output_final = f"print_ready_{user_id}.jpg"
            
            # Hojii Template-ii raawwachuu
            create_final_id_template(front, back, output_final)
            
            # Fakkii qophaa'e deebisanii erguu
            with open(output_final, 'rb') as photo:
                bot.send_photo(user_id, photo, caption="🎉 Kunoo Fayda ID keessan bifa kanaan print-fii qophaa'eera! Hojii gaarii.")
                
            # Files irraa qulqulleessuu
            os.remove(front)
            os.remove(back)
            os.remove(output_final)
            
            USER_STATES[user_id] = None
            USER_IMAGES[user_id] = {}
            del PAID_USERS[user_id]
            
        except Exception as e:
            bot.reply_to(message, f"Dogoggora uumameera: {str(e)}")

print("Botiin kee haaraatti qophaa'eera...")
bot.infinity_polling()
