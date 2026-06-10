import os
import telebot
from PIL import Image

# 🔑 CONFIGURATION
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8974775722:AAEdkBUxx02cwzLLzGT6Fa5hqSWtveqGz6A')  
ADMIN_ID = int(os.environ.get('ADMIN_CHAT_ID', 123654987))

bot = telebot.TeleBot(TOKEN)

USER_STATES = {}   
USER_IMAGES = {}   
PAID_USERS = {}    

# 🗄️ TRANSACTION DATABASE (Kaffaltii daddabalame ittisuuf)
USED_TRANSACTIONS = set()

# --- HOJII FAKKII VERTICAL ORIGINAL QAJEELCHUU ---

def crop_vertical_card(image_path, target_w=638, target_h=1011):
    """Fakkii screenshot keessaa kaardicha bifa original vertical ta'een mura"""
    img = Image.open(image_path)
    w_orig, h_orig = img.size
    
    # 1. Screenshot gubbaa fi jala irraa UI ballessuuf muruu
    left = int(w_orig * 0.05)
    top = int(h_orig * 0.15)
    right = int(w_orig * 0.95)
    bottom = int(h_orig * 0.83)
    cropped_img = img.crop((left, top, right, bottom))
    
    # 2. Aspect ratio bifa vertical ($638 \times 1011$) eeguu
    target_ratio = target_w / target_h
    crop_w, crop_h = cropped_img.size
    current_ratio = crop_w / crop_h
    
    if current_ratio > target_ratio:
        new_width = int(target_ratio * crop_h)
        offset = (crop_w - new_width) // 2
        final_cropped = cropped_img.crop((offset, 0, crop_w - offset, crop_h))
    else:
        new_height = int(crop_w / target_ratio)
        offset = (crop_h - new_height) // 2
        final_cropped = cropped_img.crop((0, offset, crop_w, crop_h - offset))
        
    return final_cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)

def create_final_id_template(front_path, back_path, output_path):
    """Kaardii fuulduraa fi duubaa qulqullinaan bifa original vertical ta'een walbira qaba"""
    front_final = crop_vertical_card(front_path)
    back_final = crop_vertical_card(back_path)
    
    # Standard CR-80 Vertical Size
    card_w, card_h = 638, 1011
    margin_x = 60  
    margin_y = 90  
    
    # Kaardii lamaan walbira fiduuf canvas bal'isuu
    canvas_w = (card_w * 2) + (margin_x * 3)
    canvas_h = card_h + (margin_y * 2)
    canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    
    # Maxxansuu (Fuuldura = Bitaa, Duuba = Mirga) bifa qajeelaan
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
    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("✅ Kaffaltii Mirkaneessi", callback_data="verify_tx"))
    bot.send_message(user_id, text, reply_markup=markup, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == "verify_tx")
def handle_callbacks(call):
    user_id = call.from_user.id
    USER_STATES[user_id] = 'Eegaa_Transaction_Number'
    bot.send_message(user_id, "✍️ Maaloo lakkoofsa daddabarsaa kaffaltii keetii (**Transaction ID / Ref Number**) guutummaatti asirratti barreessii ergi.\n\nFakkeenya: `DFA0RZLEIA` ykn `FT26162HX8P3`")


@bot.message_handler(func=lambda message: USER_STATES.get(message.from_user.id) == 'Eegaa_Transaction_Number')
def verify_transaction_number(message):
    user_id = message.from_user.id
    input_tx = message.text.strip().upper()
    
    # 🔒 CHECKER 1: Gabaabbina lakkofsichaa (Yoo gabaabaa ta'e soba)
    if len(input_tx) < 8 or not input_tx.isalnum():
        bot.reply_to(message, "❌ Dogoggora: Lakkoofsi daddabarsaa ati galchite sirrii miti ykn baay'ee gabaabaadha. Maaloo lakkofsa sirrii galchi.")
        return

    # 🔒 CHECKER 2: Duraan itti hojjetameera yoo ta'e (Gowwoomsaa)
    if input_tx in USED_TRANSACTIONS:
        bot.reply_to(message, "❌ Dogoggora: Lakkoofsi kaffaltii kun duraan tajaajila biraaf itti hojjetameera! Gowwoomsaan dhowwamaadha.")
        return
        
    # Kaffaltii dhugaa fudhachuu
    USED_TRANSACTIONS.add(input_tx)
    PAID_USERS[user_id] = True
    USER_STATES[user_id] = 'Eegaa_Fuulduraa'
    
    bot.reply_to(message, "🎉 Kaffaltiin keessan mirkanaa'eera! Amma hojii ni jalqabna.\n\n👉 Maaloo fakkii ID keetii kan *GARA FUULDURAA* (Front) ergi.")
    try:
        bot.send_message(ADMIN_ID, f"🔔 [APPROVED]: User {user_id} lakkoofsa `{input_tx}` kaffaltii raawwateera.")
    except Exception:
        pass


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
        bot.reply_to(message, "⏳ Nu eegi, fakkicha original bifa vertical qulqulluun sirreessaa jirra...")
        
        try:
            front = USER_IMAGES[user_id]['front']
            back = USER_IMAGES[user_id]['back']
            output_final = f"print_ready_{user_id}.jpg"
            
            create_final_id_template(front, back, output_final)
            
            with open(output_final, 'rb') as photo:
                bot.send_photo(user_id, photo, caption="🎉 Kunoo Fayda ID keessan bifa original kofni isaa eegameen qophaa'eera! Hojii gaarii.")
                
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
