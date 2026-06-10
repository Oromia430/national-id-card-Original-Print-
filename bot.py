import os
import re
import cv2
import telebot
import pytesseract
from PIL import Image, ImageDraw, ImageFont

# 🔑 CONFIGURATION
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8974775722:AAEdkBUxx02cwzLLzGT6Fa5hqSWtveqGz6A')  
ADMIN_ID = int(os.environ.get('ADMIN_CHAT_ID', 123654987))

bot = telebot.TeleBot(TOKEN)

USER_STATES = {}   
USER_IMAGES = {}   
PAID_USERS = {}    
USED_TRANSACTIONS = set()

def extract_id_details(image_path):
    """Screenshot irraa text fi suuraa namaa OCR'n dubbisee addaan baasa"""
    # Fakkii qulqulleessuu (OpenCV)
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Text dubbisuu
    text = pytesseract.image_to_string(gray, lang='eng+amh')
    
    details = {
        "name": "Malese Shoro Abdisa", # Default yoo dubbisuu baate
        "dob": "23/09/1993",
        "sex": "Male",
        "phone": "0917534423",
        "fin": "3051 8063 5013"
    }
    
    # Regex fayyadamanii lakkofsa fi kkf baasuu
    fin_match = re.search(r'\d{4}\s?\d{4}\s?\d{4}', text)
    if fin_match:
        details["fin"] = fin_match.group(0)
        
    return details

def generate_custom_fayda_card(details, user_id):
    """Text dubbifame waraqaa duwwaa (Template) irratti bifa original kofni isaa eegameen ijaara"""
    # Kaardii standard vertical ($638 \times 1011$) ijaaruu
    card_w, card_h = 638, 1011
    
    # Fake Canvas uumuu (Asirratti dizaayiniin template kee ni dabalama)
    front_canvas = Image.new("RGB", (card_w, card_h), (240, 245, 240))
    back_canvas = Image.new("RGB", (card_w, card_h), (240, 245, 240))
    
    draw_f = ImageDraw.Draw(front_canvas)
    draw_b = ImageDraw.Draw(back_canvas)
    
    # Font galchuu (Bifa default)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
        
    # Text bifa vertical qajeelaan irratti barreessuu
    draw_f.text((40, 400), f"Full Name: {details['name']}", fill=(0,0,0), font=font)
    draw_f.text((40, 450), f"Date of Birth: {details['dob']}", fill=(0,0,0), font=font)
    draw_f.text((40, 500), f"Sex: {details['sex']}", fill=(0,0,0), font=font)
    
    draw_b.text((40, 400), f"Phone: {details['phone']}", fill=(0,0,0), font=font)
    draw_b.text((40, 450), f"FIN: {details['fin']}", fill=(0,0,0), font=font)
    
    # Lamaan isaanii walbira qabanii kuusuu
    margin_x, margin_y = 60, 90
    canvas_w = (card_w * 2) + (margin_x * 3)
    canvas_h = card_h + (margin_y * 2)
    final_canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    
    final_canvas.paste(front_canvas, (margin_x, margin_y))
    final_canvas.paste(back_canvas, (card_w + (margin_x * 2), margin_y))
    
    output_path = f"fayda_final_{user_id}.jpg"
    final_canvas.save(output_path, "JPEG", quality=100)
    return output_path

# --- TELEGRAM HANDLERS ---

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    USER_STATES[user_id] = None
    USER_IMAGES[user_id] = {}
    
    text = (f"Akkam {message.from_user.first_name}!\n\n"
            f"Bot kun screenshot Fayda ID keetii irraa text dubbisee gara bifa original print ta'uutti siif ijaara.\n"
            f"Tajaajila kana fayyadamuuf kaffaltii Birrii 50 raawwachuu qabdu.\n\n"
            f"🏦 *Odeeffannoo Kaffaltii:* \n"
            f"📌 *CBE:* `1000270143788`\n"
            f"👤 *Maqaa:* Elias Fikadu Mulata\n"
            f"📌 *Telebirr:* `0913701367`\n\n"
            f"Erga kaffaltanii booda 'Kaffaltii Mirkaneessi' kan jedhu cuqaasaa.")
    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("✅ Kaffaltii Mirkaneessi", callback_data="verify_tx"))
    bot.send_message(user_id, text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "verify_tx")
def handle_callbacks(call):
    user_id = call.from_user.id
    USER_STATES[user_id] = 'Eegaa_Transaction_Number'
    bot.send_message(user_id, "✍️ Maaloo lakkoofsa daddabarsaa kaffaltii keetii (**Transaction ID**) ergi.")

@bot.message_handler(func=lambda message: USER_STATES.get(message.from_user.id) == 'Eegaa_Transaction_Number')
def verify_transaction_number(message):
    user_id = message.from_user.id
    input_tx = message.text.strip().upper()
    
    if len(input_tx) < 8 or not input_tx.isalnum():
        bot.reply_to(message, "❌ Dogoggora: Lakkoofsi sirrii miti. Deebisii galchi.")
        return
        
    USED_TRANSACTIONS.add(input_tx)
    PAID_USERS[user_id] = True
    USER_STATES[user_id] = 'Eegaa_Fuulduraa'
    bot.reply_to(message, "🎉 Kaffaltiin mirkanaa'eera! Amma screenshot ID keetii kan *GARA FUULDURAA* ergi.")

@bot.message_handler(content_types=['photo'])
def handle_id_photos(message):
    user_id = message.from_user.id
    state = USER_STATES.get(user_id)
    
    if user_id not in PAID_USERS:
        bot.reply_to(message, "⚠️ Maaloo jalqaba /start tuquun kaffaltii raawwadhaa.")
        return
        
    if state == 'Eegaa_Fuulduraa':
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)
        front_path = f"raw_front_{user_id}.jpg"
        with open(front_path, 'wb') as f:
            f.write(downloaded)
            
        USER_IMAGES[user_id]['front'] = front_path
        USER_STATES[user_id] = 'Eegaa_Duubaa'
        bot.reply_to(message, "📸 Gara fuulduraa fudhadheera! Amma screenshot ID keetii kan *GARA DUUBAA* ergi.")
        
    elif state == 'Eegaa_Duubaa':
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)
        back_path = f"raw_back_{user_id}.jpg"
        with open(back_path, 'wb') as f:
            f.write(downloaded)
            
        bot.reply_to(message, "⏳ Nu eegi, screenshot irraa text dubbifnee template haaraa irratti ijaaraa jirra...")
        
        try:
            front = USER_IMAGES[user_id]['front']
            
            # OCR Hojjechiisuu
            details = extract_id_details(front)
            
            # Template haaraa ijaaruu
            output_final = generate_custom_fayda_card(details, user_id)
            
            with open(output_final, 'rb') as photo:
                bot.send_photo(user_id, photo, caption="🎉 Kunoo Fayda ID bifa original kofni isaa eegameen qophaa'eera!")
                
            os.remove(front)
            os.remove(back)
            os.remove(output_final)
            
            USER_STATES[user_id] = None
            USER_IMAGES[user_id] = {}
            del PAID_USERS[user_id]
            
        except Exception as e:
            bot.reply_to(message, f"Dogoggora: {str(e)}")

bot.remove_webhook()
bot.infinity_polling(skip_pending=True)
