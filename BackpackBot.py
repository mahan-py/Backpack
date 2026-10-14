import telebot
import asyncio
from telebot import types
from telebot.apihelper import ApiTelegramException
import Backpack
import sqlite3
import time
from datetime import date
from pathlib import Path

# Some messages were too long so i created txt files and wrote them there
with open("Bot_help.txt", "r", encoding= "utf-8") as file2:
	help_message = file2.read()	

# Bot-token
bot = telebot.TeleBot("BOT-TOKEN")

# Users have to join these channels if they want to use the bot
Backpack_Channel = "@Backpacktool"
Artplus = "@ArtplusT"

# This function checks users membership
def check_membership(user_id):
	try:
		Target_user_status = ["member", "administrator", "creator"]
		member1 = bot.get_chat_member("@Backpacktool", user_id)
		member2 = bot.get_chat_member("@ArtplusT", user_id)
		if not (member1.status in Target_user_status and member2.status in Target_user_status):
			return False
		else: 
			return True	
	except:
		return "Problem"

# If the users have not joined the channels
def send_membership_message(chat_id):
	Channels_markup = types.InlineKeyboardMarkup(row_width= 2)
	channel1_button = types.InlineKeyboardButton("کانال 1", url= "https://t.me/Backpacktool", style= "primary")
	channel2_button = types.InlineKeyboardButton("کانال 2", url= "https://t.me/ArtplusT", style= "primary")
	check_button = types.InlineKeyboardButton("بررسی عضویت", callback_data= "check_membership", style= "success")
	Channels_markup.add(
		channel1_button, channel2_button,
		check_button,
	)		
	bot.send_message(chat_id, "برای استفاده از ربات عضو چنل های زیر شوید", reply_markup= Channels_markup)

# When users click on check membership button this function checks the membership again
@bot.callback_query_handler(func= lambda call: call.data == "check_membership")
def restart_checking_membership(call):
	if check_membership(call.from_user.id):
		bot.answer_callback_query(call.id, "عضویت تایید شد")
		bot.delete_message(call.message.chat.id, call.message.message_id)	
	else:
		bot.answer_callback_query(call.id, "هنوز عضو نیستید!", show_alert= True)			


# Database section
# Base dir of database
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "bot.db"

conn = sqlite3.connect(DB_PATH, timeout=10)
cursor = conn.cursor()
cursor.execute("""
	CREATE TABLE IF NOT EXISTS users(
	user_id INTEGER PRIMARY KEY, is_premium BOOLEAN NOT NULL DEFAULT 0
	)
""")

cursor.execute("""
	CREATE TABLE IF NOT EXISTS admins (
	user_id INTEGER PRIMARY KEY
	)
""")
conn.commit()
conn.close()

def get_database():
	return sqlite3.connect(DB_PATH, timeout= 10)

def is_admin(user_id):
	conn = get_database()
	cursor = conn.cursor()
	cursor.execute("SELECT 1 FROM admins WHERE user_id = ?", (user_id,))
	result = cursor.fetchone()
	conn.close()
	return result is not None


# Admin panel
bot_owners = ["IronAryan"]

admin_keyboard = types.InlineKeyboardMarkup(row_width= 2)
admins_button = types.InlineKeyboardButton("ادمین💎", callback_data= "admins")
log_button = types.InlineKeyboardButton("لاگ ربات⚠️", callback_data= "show_log")
users_button = types.InlineKeyboardButton("کاربران👤", callback_data= "users")
send_broadcast_button = types.InlineKeyboardButton("پیام همگانی✉️", callback_data= "Broadcast")
premium_button = types.InlineKeyboardButton("پریمیوم💸", callback_data= "premium")
admin_keyboard.add(
	admins_button, log_button,
	users_button, premium_button,
	send_broadcast_button,
)

@bot.message_handler(commands= ['admin'], func= lambda message: message.chat.type == "private")
def check_admin(message):
	if is_admin(message.from_user.id) == False and message.from_user.username not in bot_owners:
		bot.reply_to(message, "❌شما ادمین نیستید و به پنل دسترسی ندارید")
	elif is_admin(message.from_user.id) == True or message.from_user.username in bot_owners:
		bot.reply_to(message, "به پنل ادمین خوش اومدید. همه چیز را اینجا مدیریت کنید", reply_markup= admin_keyboard)	

@bot.callback_query_handler(func= lambda call: call.data == "admins")
def admin_management(call):
	conn = get_database()
	cursor = conn.cursor()
	cursor.execute("SELECT user_id FROM admins")
	admins = cursor.fetchall()
	conn.close()

	admin_management_keyboard = types.InlineKeyboardMarkup(row_width= 1)
	add_admin = types.InlineKeyboardButton("اضافه کردن ادمین", callback_data= "add_adminstator", style= "primary")
	delete_admin = types.InlineKeyboardButton("حذف کردن ادمین", callback_data= "delete_adminstator", style= "danger")
	go_back_button = types.InlineKeyboardButton("برگشت به منو", callback_data= "admin_panel")
	admin_management_keyboard.add(add_admin, delete_admin, go_back_button,)
	if admins:
		text = "⚜️لیست ادمین ها:\n\n"
		for admin in admins:
			text += f"🆔`{admin[0]}`\n"
	else:
		text = "❌هیچ ادمینی ثبت نشده"
	
	bot.answer_callback_query(call.id)	
	bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup= admin_management_keyboard, parse_mode= "Markdown")

@bot.callback_query_handler(func= lambda call: call.data == "admin_panel")				
def back_admin_panel(call):
	bot.answer_callback_query(call.id)
	bot.edit_message_text("از منوی زیر انتخاب کنید", call.message.chat.id, call.message.message_id,reply_markup= admin_keyboard)
@bot.callback_query_handler(func= lambda call: call.data == "add_adminstator")
def get_adminstator_id(call):
	bot.answer_callback_query(call.id)
	bot.send_message(call.message.chat.id, "آیدی عددی کاربر مورد نظر را ارسال کنید")
	bot.register_next_step_handler(call.message, add_adminstator)
def add_adminstator(message):
	admin_management_keyboard = types.InlineKeyboardMarkup(row_width= 1)
	add_admin = types.InlineKeyboardButton("اضافه کردن ادمین", callback_data= "add_adminstator", style= "primary")
	delete_admin = types.InlineKeyboardButton("حذف کردن ادمین", callback_data= "delete_adminstator", style= "danger")
	go_back_button = types.InlineKeyboardButton("برگشت به منو", callback_data= "admin_panel")
	admin_management_keyboard.add(add_admin, delete_admin, go_back_button,)
	
	conn = get_database()
	cursor = conn.cursor()
	cursor.execute("""INSERT OR IGNORE INTO admins (user_id) VALUES (?)""", (message.text,))
	conn.commit()
	conn.close()
	bot.send_message(message.chat.id, "عملیات با موفقیت انجام شد✅", reply_markup= admin_management_keyboard)
@bot.callback_query_handler(func= lambda call: call.data == "delete_adminstator")
def get_adminstator_id_delete(call):
	bot.answer_callback_query(call.id)
	bot.send_message(call.message.chat.id, "آیدی عددی کاربر مورد نظر را ارسال کنید")
	bot.register_next_step_handler(call.message, delete_adminstator)
def delete_adminstator(message):
	admin_management_keyboard = types.InlineKeyboardMarkup(row_width= 1)
	add_admin = types.InlineKeyboardButton("اضافه کردن ادمین", callback_data= "add_adminstator", style= "primary")
	delete_admin = types.InlineKeyboardButton("حذف کردن ادمین", callback_data= "delete_adminstator", style= "danger")
	go_back_button = types.InlineKeyboardButton("برگشت به منو", callback_data= "admin_panel")
	admin_management_keyboard.add(add_admin, delete_admin, go_back_button,)

	conn = get_database()
	cursor = conn.cursor()
	cursor.execute("DELETE FROM admins WHERE user_id = ?", (message.text,))
	conn.commit()
	conn.close()
	bot.send_message(message.chat.id, "عملیات با موفقیت انجام شد✅", reply_markup= admin_management_keyboard)

@bot.callback_query_handler(func= lambda call: call.data == "show_log")
def send_log(call):
	try:
		with open("bot.log", "rb") as log_file:
			bot.send_chat_action(call.message.chat.id, "upload_document")
			bot.send_document(call.message.chat.id, log_file)
			bot.answer_callback_query(call.id)
	except Exception:
		bot.answer_callback_query(call.id)
		bot.send_message(call.message.chat.id, "❌خطا در ارسال فایل لاگ")		

@bot.callback_query_handler(func= lambda call: call.data == "users")
def send_users_info(call):
	admin_management_keyboard = types.InlineKeyboardMarkup(row_width= 1)
	go_back_button = types.InlineKeyboardButton("برگشت به منو", callback_data= "admin_panel", style= "danger")
	admin_management_keyboard.add(go_back_button)

	conn = get_database()
	cursor = conn.cursor()
	cursor.execute("SELECT COUNT(*) FROM users")
	total_users = cursor.fetchone()[0]
	cursor.execute("SELECT COUNT(*) FROM users WHERE is_premium != 0")
	premium_users = cursor.fetchone()[0]
	conn.close()
	text = f"🟦آمار کل کاربران\n\nتعداد کل: {total_users}\nکاربران پریمیوم: {premium_users}"
	bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup= admin_management_keyboard)
	bot.answer_callback_query(call.id)

@bot.callback_query_handler(func= lambda call: call.data == "Broadcast")
def get_admin_message(call):
	admin_management_keyboard = types.InlineKeyboardMarkup(row_width= 1)
	go_back_button = types.InlineKeyboardButton("لغو", callback_data= "cancel_broadcast", style= "danger")
	admin_management_keyboard.add(go_back_button)

	bot.answer_callback_query(call.id)
	bot.send_message(call.message.chat.id, "پیامی که میخواید به تمام کاربرای بات بفرستید ارسال کنید", reply_markup= admin_management_keyboard)
	bot.register_next_step_handler(call.message, send_broadcast)
def send_broadcast(message):
	conn = get_database()
	cursor = conn.cursor()
	cursor.execute("SELECT user_id FROM users")
	all_users = cursor.fetchall()
	conn.close()	
	success = 0
	failed = 0
	for (user_id,) in all_users:
		while True:	
			try:
				bot.copy_message(user_id, message.chat.id, message.message_id)
				success += 1
				break
			except ApiTelegramException as e:
				if e.error_code == 429:
					retry_after = e.result_json["parameters"]["retry_after"]
					time.sleep(retry_after)
					continue
				else:
					failed += 1
					break
	bot.send_message(message.chat.id, f"عملیات با موفقیت انجام شد\nتعداد کل کاربران: {len(all_users)}\nتعداد پیام های ارسال شده: {success}\nپیام های ارسال نشده: {failed}")			
@bot.callback_query_handler(func= lambda call: call.data == "cancel_broadcast")
def cancel_broadcast(call):
	bot.clear_step_handler_by_chat_id(call.message.chat.id)
	bot.answer_callback_query(call.id)
	bot.delete_message(call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func= lambda call: call.data == "premium")
def get_premium_user_id(call):
	admin_management_keyboard = types.InlineKeyboardMarkup(row_width= 1)
	go_back_button = types.InlineKeyboardButton("لغو", callback_data= "cancel_broadcast", style= "danger")
	admin_management_keyboard.add(go_back_button)

	bot.answer_callback_query(call.id)
	bot.send_message(call.message.chat.id, "آیدی کاربری که میخواید پریمیوم بشه رو ارسال کنید", reply_markup= admin_management_keyboard)
	bot.register_next_step_handler(call.message, set_premium_user)
def set_premium_user(message):
	admin_management_keyboard = types.InlineKeyboardMarkup(row_width= 1)
	go_back_button = types.InlineKeyboardButton("برگشت به منو", callback_data= "admin_panel", style= "danger")
	admin_management_keyboard.add(go_back_button)

	today = date.today()
	try:
		premium_until = today.replace(year=today.year + 1)
	except ValueError:
		premium_until = today.replace(year=today.year + 1, day=28)
	
	premium_until = premium_until.isoformat()
	
	conn = get_database()
	cursor = conn.cursor()
	cursor.execute("""UPDATE users SET is_premium = ? WHERE user_id = ?""", (premium_until, message.text))
	conn.commit()
	updated = cursor.rowcount
	conn.close()
	if updated == 0:
		bot.send_message(message.chat.id, "کاربری با این آیدی پیدا نشد❌", reply_markup= admin_management_keyboard)
	else:
		bot.send_message(message.chat.id, f"اشتراک پریمیوم با موفقیت فعال شد✅\n\nآیدی کاربر: `{message.text}`\nنوع اشتراک: یک ساله\nتاریخ انقضا: {premium_until}", parse_mode= "Markdown", reply_markup= admin_management_keyboard)			


# Main keyboard buttons
keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
average_button = types.KeyboardButton("میانگین🧮")
bmi_button = types.KeyboardButton("BMI🏋🏻‍♂️")
currency_button = types.KeyboardButton("قیمت ارز💰")
password_button = types.KeyboardButton("تولید رمز🔑")
date_difference_button = types.KeyboardButton("اختلاف تاریخ📅")
lottery_button = types.KeyboardButton("قرعه کشی⚜️")
format_converter_button = types.KeyboardButton("تبدیل فرمت📁")
text_to_speech_button = types.KeyboardButton("متن به صوت🎙")
user_info_button = types.KeyboardButton("تلگرام من👤")
inline_keyboard_maker_button = types.KeyboardButton("دکمه شیشه ای🍷")
keyboard.add(
	average_button, bmi_button,
	currency_button, password_button,
	date_difference_button, lottery_button, 
	format_converter_button, text_to_speech_button, 
	user_info_button, inline_keyboard_maker_button,
)

# Starting the bot for the first time or reaction to /start
@bot.message_handler(commands=['start'], func= lambda message: message.chat.type == "private")
def send_welcome(message):

	conn = get_database()
	cursor = conn.cursor()
	cursor.execute("INSERT OR IGNORE INTO users(user_id) VALUES (?)", (message.from_user.id,))
	conn.commit()
	conn.close()

	if not check_membership(message.from_user.id):
		send_membership_message(message.chat.id)
	else:
		user_first_name = message.from_user.first_name	
		bot.send_message(message.chat.id, f"⚜️سلام {user_first_name} عزیز! ابزاری که نیاز داری رو از منوی زیر انتخاب کن\nبرای راهنمایی /help رو ارسال کن", reply_markup= keyboard)

# Sends a general guide to help users
@bot.message_handler(commands=['help'], func= lambda message: message.chat.type == "private")
def send_help(message):
	bot.reply_to(message, help_message)


# Average button run
@bot.message_handler(func= lambda message: message.text == "میانگین🧮" and message.chat.type == "private")
def average_tool(message):
	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	Cancel_markup.add(Cancel_button)
	if not check_membership(message.from_user.id):
		send_membership_message(message.chat.id)
	else:	
		bot.reply_to(message, "لطفا اعداد را بدون علامت های ریاضی و حروف ارسال کنید", reply_markup= Cancel_markup)
		bot.register_next_step_handler(message, get_numbers)

def get_numbers(message):
	try:
		numbers = message.text
		average = Backpack.takes_average(numbers)
		bot.send_message(message.chat.id, average)
	except:
		bot.send_message(message.chat.id, "مشکلی پیش اومد")	

# BMI button run
@bot.message_handler(func= lambda message: message.text == "BMI🏋🏻‍♂️" and message.chat.type == "private")
def bmi_tool(message):
	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	Cancel_markup.add(Cancel_button)
	if not check_membership(message.from_user.id):
		send_membership_message(message.chat.id)
	else:
		bot.reply_to(message, "وزن خود را به کیلوگرم ارسال کنید", reply_markup= Cancel_markup)
		bot.register_next_step_handler(message, get_weight)

def restart_getting_weight(message):
	bot.clear_step_handler_by_chat_id(message.chat.id)
	bot.send_message(message.chat.id, "وزن خود را به کیلوگرم ارسال کنید")
	bot.register_next_step_handler(message, get_weight)

def get_weight(message):
	Cancel_markup = types.InlineKeyboardMarkup()
	back_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	back_button = types.InlineKeyboardButton("مرحله قبل", callback_data= "Back")
	Cancel_markup.add(Cancel_button)
	back_markup.add(back_button, Cancel_button)
	try:
		weight = float(message.text)
		if not 20 <= weight <= 300:
			bot.reply_to(message, "وزن باید بین 20 تا 300 کیلوگرم باشد ، دوباره ارسال کنید", reply_markup= Cancel_markup)
			bot.register_next_step_handler(message, get_weight)
		else:
			bot.reply_to(message, "قد خود را بر حسب متر ارسال کنید", reply_markup= back_markup)	
			bot.register_next_step_handler(message, get_height, weight)
	except ValueError:
		bot.reply_to(message, "لطفا فقط عدد ارسال کنید", reply_markup= Cancel_markup)
		bot.register_next_step_handler(message, get_weight)

# Cancels everything and replys to main keyboard, every where you see cancel call back query it's related to here
@bot.callback_query_handler(func= lambda call: call.data == "cancel")
def cancel_handler(call):
	bot.clear_step_handler_by_chat_id(call.message.chat.id)
	bot.answer_callback_query(call.id)
	bot.send_message(call.message.chat.id, "ابزار مورد نظر را انتخاب کنید", reply_markup= keyboard)
# Go back button related to BMI calculator tool
@bot.callback_query_handler(func= lambda call: call.data == "Back")
def back_handler(call):
		bot.answer_callback_query(call.id)
		restart_getting_weight(call.message)
	
def get_height(message, weight):
	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	Cancel_markup.add(Cancel_button)
	try:
		height = float(message.text)
		if not 1.20 <= height <= 2.50:
			bot.reply_to(message, "قد باید بین 1.20 متر و 2.50 متر باشد ، دوباره ارسال کنید", reply_markup= Cancel_markup)
			bot.register_next_step_handler(message, get_height, weight)
		else:
			user_BMI = Backpack.bmi(weight, height)

			bmi_information_sources = types.InlineKeyboardMarkup()
			source = types.InlineKeyboardButton("اطلاعات بیشتر", url= "https://fa.wikipedia.org/wiki/%D8%B4%D8%A7%D8%AE%D8%B5_%D8%AA%D9%88%D8%AF%D9%87_%D8%A8%D8%AF%D9%86%DB%8C")
			bmi_information_sources.add(source)

			bot.send_message(message.chat.id, user_BMI, reply_markup= bmi_information_sources)	
	except ValueError:
		bot.reply_to(message, "لطفا عدد ارسال کنید")
		bot.register_next_step_handler(message, get_height, weight)

# Prices button run
@bot.message_handler(func= lambda message: message.text == "قیمت ارز💰" and message.chat.type == "private")
def choose_currency(message):
	currency_keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
	dollar_burron = types.KeyboardButton("دلار")
	euro_button = types.KeyboardButton("یورو")
	gold_button = types.KeyboardButton("طلا")
	bitcoin_button = types.KeyboardButton("بیت کوین")
	tether_button = types.KeyboardButton("تتر")
	gram_button = types.KeyboardButton("گرام")
	solana_button = types.KeyboardButton("سولانا")
	ethereum_button = types.KeyboardButton("اتریوم")
	ripple_button = types.KeyboardButton("ریپل")
	currency_keyboard.add(
			dollar_burron, tether_button, gold_button,
			euro_button, bitcoin_button, gram_button,
			solana_button, ethereum_button, ripple_button
	)

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("برگشت به منوی اصلی", callback_data= "cancel", style= "danger")
	Cancel_markup.add(Cancel_button)

	if not check_membership(message.from_user.id):
		send_membership_message(message.chat.id)
	else:	
		bot.reply_to(message, "ارز مورد نظر را از منوی زیر انتخاب کنید", reply_markup= currency_keyboard)
		bot.send_message(message.chat.id, "اگر ارز مورد نظر در منو نیست ، اسم کامل آن را به فارسی ارسال کنید", reply_markup= Cancel_markup)
		bot.register_next_step_handler(message, find_price)

def find_price(message):

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("برگشت به منوی اصلی", callback_data= "cancel", style= "danger")
	Cancel_markup.add(Cancel_button)

	currency_name = message.text
	price = Backpack.APIprices(currency_name)
	bot.reply_to(message, price, reply_markup= Cancel_markup)
	bot.register_next_step_handler(message, find_price)

# Password generator
@bot.message_handler(func= lambda message: message.text == "تولید رمز🔑" and message.chat.type == "private")
def get_password_type(message):
	password_generator_keyboard = types.ReplyKeyboardMarkup(row_width= 1, resize_keyboard= True)
	number_button = types.KeyboardButton("فقط شامل اعداد")
	letter_button = types.KeyboardButton("فقط شامل حروف")
	mix_button = types.KeyboardButton("ترکیبی")
	cancel_button = types.KeyboardButton("لغو")
	password_generator_keyboard.add(
		number_button,
		letter_button,
		mix_button,
		cancel_button,
	)
	if not check_membership(message.from_user.id):
		send_membership_message(message.chat.id)
	else:	
		bot.reply_to(message, "نوع رمز را از منوی زیر وارد کنید", reply_markup= password_generator_keyboard)
		bot.register_next_step_handler(message, check_type)

def check_type(message):
	if message.text not in ["فقط شامل اعداد", "فقط شامل حروف", "ترکیبی", "لغو"]:
		bot.send_message(message.chat.id, "لطفا از منوی زیر انتخاب کنید")
		bot.register_next_step_handler(message, check_type)
	elif message.text == "لغو":
		bot.clear_step_handler_by_chat_id(message.chat.id)
		bot.send_message(message.chat.id, "ابزار مورد نظر را انتخاب کنید", reply_markup= keyboard)	
	else:
		back_markup = types.InlineKeyboardMarkup()
		back_button = types.InlineKeyboardButton("مرحله قبل", callback_data= "check_type_back", style= "primary")
		back_markup.add(back_button)
		password_type = message.text
		bot.reply_to(message, "تعداد کاراکتر رمز را وارد کنید", reply_markup= back_markup)
		bot.register_next_step_handler(message, charachter, password_type)	

def charachter(message, password_type):
	if message.text == "لغو":
		bot.clear_step_handler_by_chat_id(message.chat.id)
		bot.send_message(message.chat.id, "ابزار مورد نظر را انتخاب کنید", reply_markup= keyboard)
	elif not 4 <= int(message.text) <= 20:
		bot.reply_to(message, "تعداد کاراکتر باید بین 4 تا 20 باشد")
		bot.register_next_step_handler(message, charachter, password_type)	
	else:
		charachter_number = message.text
		create_password(message, password_type, charachter_number)	

def create_password(message, password_type, charachter_number):
	length = int(charachter_number)
	if password_type == "فقط شامل اعداد":
		user_password = Backpack.NumbericPasswordGenerator()
		result = user_password.generate_password(length= length)
		bot.send_message(message.chat.id, result, reply_markup= keyboard)
	elif password_type == "فقط شامل حروف":
		user_password = Backpack.LetterPasswordGenerator()
		result = user_password.generate_password(length= length)
		bot.send_message(message.chat.id, result, reply_markup= keyboard)
	elif password_type == "ترکیبی":
		user_password = Backpack.MixedPasswordGenerator()
		result = user_password.generate_password(length= length)
		bot.send_message(message.chat.id, result, reply_markup= keyboard)		

# When users want to choose password type again
@bot.callback_query_handler(func= lambda call: call.data == "check_type_back")
def restart_get_password_type(call):
	bot.clear_step_handler_by_chat_id(call.message.chat.id)
	bot.answer_callback_query(call.id)
	get_password_type(call.message)

# Date difference button run
@bot.message_handler(func= lambda message: message.text == "اختلاف تاریخ📅" and message.chat.type == "private")
def get_date_type(message):
	
	Cancel_markup = types.InlineKeyboardMarkup(row_width= 2)
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	English_date_button = types.InlineKeyboardButton("میلادی", callback_data= "CE")
	Persian_date_button = types.InlineKeyboardButton("شمسی", callback_data= "sun")
	Cancel_markup.add(
		Persian_date_button, English_date_button,
		Cancel_button
	)
	if not check_membership(message.from_user.id):
		send_membership_message(message.chat.id)
	else:	
		bot.send_message(message.chat.id, "نوع تاریخ را انتخاب کنید", reply_markup= Cancel_markup)

# Persian date requirements related to next function
import jdatetime	
now = jdatetime.date.today()
present_year = now.year
present_month = now.month
present_day = now.day

# When users choose Persian date type
@bot.callback_query_handler(func= lambda call: call.data == "sun")
def persian_date_get_year(call):
	
	bot.answer_callback_query(call.id)
	bot.clear_step_handler_by_chat_id(call.message.chat.id)
	get_year(call.message)
def get_year(message):

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	Cancel_markup.add(Cancel_button)

	send_message = bot.send_message(message.chat.id, "سال مورد نظر را وارد کنید", reply_markup= Cancel_markup)
	bot.register_next_step_handler(send_message, year_check)


def year_check(message):

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	Cancel_markup.add(Cancel_button)
	try:
		if len(message.text) < 4 or len(message.text) > 4 or int(message.text) > present_year:
			bot.reply_to(message, "سال باید معتبر و کمتر از سال حاضر باشد ، دوباره ارسال کنید", reply_markup= Cancel_markup)
			bot.register_next_step_handler(message, year_check)
		else: 
			year = int(message.text)
			get_month(message, year)
	except ValueError:
		bot.reply_to(message, "فقط عدد ارسال کنید", reply_markup= Cancel_markup)
		bot.register_next_step_handler(message, year_check)		

def get_month(message, year):
	date_keyboard = types.ReplyKeyboardMarkup(row_width= 3, resize_keyboard= True)
	month1_button = types.KeyboardButton("فروردین")
	month2_button = types.KeyboardButton("اردیبهشت")
	month3_button = types.KeyboardButton("خرداد")
	month4_button = types.KeyboardButton("تیر")
	month5_button = types.KeyboardButton("مرداد")
	month6_button = types.KeyboardButton("شهریور")
	month7_button = types.KeyboardButton("مهر")
	month8_button = types.KeyboardButton("آبان")
	month9_button = types.KeyboardButton("آذر")
	month10_button = types.KeyboardButton("دی")
	month11_button = types.KeyboardButton("بهمن")
	month12_button = types.KeyboardButton("اسفند")
	date_keyboard.add(
		month3_button, month2_button, month1_button,
		month6_button, month5_button, month4_button,
		month9_button, month8_button, month7_button,
		month12_button, month11_button, month10_button,
	)

	bot.send_message(message.chat.id, "از لیست ماه مورد نظر را انتخاب کنید", reply_markup= date_keyboard)
	bot.register_next_step_handler(message, month_check, year)

def month_check(message, year):

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_back_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	back_button = types.InlineKeyboardButton("مرحله قبل", callback_data= "sun_back_to_get_year", style= "primary")
	Cancel_markup.add(Cancel_button)
	Cancel_back_markup.add(Cancel_button, back_button)

	months = {"فروردین" : 1, "اردیبهشت" : 2, "خرداد" : 3, "تیر" : 4, "مرداد" : 5, "شهریور" : 6, "مهر" : 7, "آبان" : 8, "آذر" : 9, "دی" : 10, "بهمن" : 11, "اسفند" : 12}
	try:
		if message.text not in months:
			bot.reply_to(message, "اسم ماه معتبر ارسال کنید", reply_markup= Cancel_markup)
			bot.register_next_step_handler(message, month_check, year)
		elif year == present_year and months[message.text] > present_month:
			bot.reply_to(message, "سالی که وارد کردید با سال حاضر برابر است پس ماه نباید از ماه حاضر بیشتر باشد ، دوباره ارسال کنید", reply_markup= Cancel_back_markup)
			bot.register_next_step_handler(message, month_check, year)
		else:
			day_get(message, year)
	except ValueError:
		bot.reply_to(message, "لطفا اسم ماه درست را انتخاب کنید", reply_markup= Cancel_markup)
		bot.register_next_step_handler(message, year)	

def day_get(message, year):

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	Cancel_markup.add(Cancel_button)

	months = {"فروردین" : 1, "اردیبهشت" : 2, "خرداد" : 3, "تیر" : 4, "مرداد" : 5, "شهریور" : 6, "مهر" : 7, "آبان" : 8, "آذر" : 9, "دی" : 10, "بهمن" : 11, "اسفند" : 12}
	month = months[message.text]
	bot.send_message(message.chat.id, "روز مورد نظر را ارسال کنید", reply_markup= Cancel_markup)
	bot.register_next_step_handler(message, day_check, year, month)

def day_check(message, year, month):

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_back_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	Cancel_markup.add(Cancel_button)
	Cancel_back_markup.add(Cancel_button)

	try:
		if year == present_year and month == present_month and int(message.text) > present_day:
			bot.reply_to(message, (f"ماه و سالی که ارسال کردید با ماه و سال حال حاضر برابر است ، پس روز نباید از {present_day} بیشتر باشد"), reply_markup= Cancel_markup)
			bot.register_next_step_handler(message, day_check, year, month)
		elif month in [1, 2, 3, 4, 5, 6] and not 1 <= int(message.text) <= 31:
			bot.reply_to(message, "تعداد روز در این ماه باید بین 1 تا 31 روز باشد ، دوباره ارسال کنید", reply_markup= Cancel_markup)
			bot.register_next_step_handler(message, day_check, year, month)
		elif month in [7, 8, 9, 10, 11] and not 1 <= int(message.text) <= 30:
			bot.reply_to(message, "تعداد روز در این ماه باید بین 1 تا 30 روز باشد ، دوباره ارسال کنید", reply_markup= Cancel_markup)
			bot.register_next_step_handler(message, day_check, year, month)
		elif month == 12:
			if not (year % 400 ==0) or (year % 100 != 0) and (year % 4 == 0):
				if not 1 <= int(message.text) <= 29:
					bot.reply_to(message, "سالی که ارسال کردید کبیسه نیست و روز باید بین 1 تا 29 باشد ، دوباره ارسال کنید", reply_markup= Cancel_markup)
					bot.register_next_step_handler(message, day_check, year, month)
			elif (year % 400 ==0) or (year % 100 != 0) and (year % 4 == 0):
				if not 1 <= int(message.text) <= 30:
					bot.reply_to(message, "سالی که ارسال کردید کبیسه است و تعداد روز باید بین 1 تا 30 باشد ، دوباره ارسال کنید", reply_markup= Cancel_markup)
					bot.register_next_step_handler(message, day_check, year, month)
		else:
			day = int(message.text)
			calculate_date_difference(message, year, month, day)
	except ValueError:
		bot.reply_to(message, "فقط عدد ارسال کنید", reply_markup= Cancel_markup)
		bot.register_next_step_handler(message, day_check, year, month)		

def calculate_date_difference(message, year, month, day):															
	result = Backpack.shamsi_date_difference(year, month, day)
	bot.send_message(message.chat.id, result, reply_markup= keyboard)

# CE date requirements related to next function
import datetime
from Backpack import date_difference_CE
now_CE = datetime.date.today()
present_CE_year = now_CE.year
present_CE_month = now_CE.month
present_CE_day = now_CE.day

# When users choose CE date type
@bot.callback_query_handler(func= lambda call: call.data == "CE")
def CE_date_get_year(call):
	
	bot.answer_callback_query(call.id)
	bot.clear_step_handler_by_chat_id(call.message.chat.id)
	get_year_CE(call.message)
def get_year_CE(message):

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	Cancel_markup.add(Cancel_button)

	send_message = bot.send_message(message.chat.id, "سال مورد نظر را وارد کنید", reply_markup= Cancel_markup)
	bot.register_next_step_handler(send_message, year_check_CE)


def year_check_CE(message):

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	Cancel_markup.add(Cancel_button)
	try:
		if len(message.text) < 4 or len(message.text) > 4 or int(message.text) > present_CE_year:
			bot.reply_to(message, "سال باید معتبر و کمتر از سال حاضر باشد ، دوباره ارسال کنید", reply_markup= Cancel_markup)
			bot.register_next_step_handler(message, year_check_CE)
		else: 
			year = int(message.text)
			get_month_CE(message, year)
	except ValueError:
		bot.reply_to(message, "فقط عدد ارسال کنید", reply_markup= Cancel_markup)
		bot.register_next_step_handler(message, year_check_CE)		

def get_month_CE(message, year):
	date_keyboard = types.ReplyKeyboardMarkup(row_width= 3, resize_keyboard= True)
	month1_button = types.KeyboardButton("January")
	month2_button = types.KeyboardButton("February")
	month3_button = types.KeyboardButton("March")
	month4_button = types.KeyboardButton("April")
	month5_button = types.KeyboardButton("May")
	month6_button = types.KeyboardButton("June")
	month7_button = types.KeyboardButton("July")
	month8_button = types.KeyboardButton("August")
	month9_button = types.KeyboardButton("September")
	month10_button = types.KeyboardButton("October")
	month11_button = types.KeyboardButton("November")
	month12_button = types.KeyboardButton("December")
	date_keyboard.add(
		month3_button, month2_button, month1_button,
		month6_button, month5_button, month4_button,
		month9_button, month8_button, month7_button,
		month12_button, month11_button, month10_button,
	)

	bot.send_message(message.chat.id, "از لیست ماه مورد نظر را انتخاب کنید", reply_markup= date_keyboard)
	bot.register_next_step_handler(message, month_check_CE, year)

def month_check_CE(message, year):

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_back_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	back_button = types.InlineKeyboardButton("مرحله قبل", callback_data= "sun_back_to_get_year", style= "primary")
	Cancel_markup.add(Cancel_button)
	Cancel_back_markup.add(Cancel_button, back_button)

	months = {"JANUARY" : 1, "FEBRUARY" : 2, "MARCH" : 3, "APRIL" : 4, "MAY" : 5, "JUNE" : 6, "JULY" : 7, "AUGUST" : 8, "SEPTEMBER" : 9, "OCTOBER" : 10, "NOVEMBER" : 11, "DECEMBER" : 12}
	try:
		if message.text.upper() not in months:
			bot.reply_to(message, "اسم ماه معتبر ارسال کنید", reply_markup= Cancel_markup)
			bot.register_next_step_handler(message, month_check_CE, year)
		elif year == present_CE_year and months[message.text.upper()] > present_CE_month:
			bot.reply_to(message, "سالی که وارد کردید با سال حاضر برابر است پس ماه نباید از ماه حاضر بیشتر باشد ، دوباره ارسال کنید", reply_markup= Cancel_back_markup)
			bot.register_next_step_handler(message, month_check_CE, year)
		else:
			day_get_CE(message, year)
	except ValueError:
		bot.reply_to(message, "لطفا اسم ماه درست را انتخاب کنید", reply_markup= Cancel_markup)
		bot.register_next_step_handler(message, month_check_CE, year)	

def day_get_CE(message, year):

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	Cancel_markup.add(Cancel_button)

	months = {"JANUARY" : 1, "FEBRUARY" : 2, "MARCH" : 3, "APRIL" : 4, "MAY" : 5, "JUNE" : 6, "JULY" : 7, "AUGUST" : 8, "SEPTEMBER" : 9, "OCTOBER" : 10, "NOVEMBER" : 11, "DECEMBER" : 12}
	month = months[message.text.upper()]
	bot.send_message(message.chat.id, "روز مورد نظر را ارسال کنید", reply_markup= Cancel_markup)
	bot.register_next_step_handler(message, day_check_CE, year, month)

def day_check_CE(message, year, month):

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_back_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	Cancel_markup.add(Cancel_button)
	Cancel_back_markup.add(Cancel_button)

	try:
		if year == present_CE_year and month == present_CE_month and int(message.text) > present_CE_day:
			bot.reply_to(message, (f"ماه و سالی که ارسال کردید با ماه و سال حال حاضر برابر است ، پس روز نباید از {present_CE_day} بیشتر باشد"), reply_markup= Cancel_markup)
			bot.register_next_step_handler(message, day_check_CE, year, month)
		elif month in [1, 3, 5, 7, 8, 10, 12] and not 1 <= int(message.text) <= 31:
			bot.reply_to(message, "تعداد روز در این ماه باید بین 1 تا 31 روز باشد ، دوباره ارسال کنید", reply_markup= Cancel_markup)
			bot.register_next_step_handler(message, day_check_CE, year, month)
		elif month in [4, 6, 9, 11] and not 1 <= int(message.text) <= 30:
			bot.reply_to(message, "تعداد روز در این ماه باید بین 1 تا 30 روز باشد ، دوباره ارسال کنید", reply_markup= Cancel_markup)
			bot.register_next_step_handler(message, day_check_CE, year, month)
		elif month == 12:
			if not (year % 400 ==0) or (year % 100 != 0) and (year % 4 == 0):
				if not 1 <= int(message.text) <= 28:
					bot.reply_to(message, "سالی که ارسال کردید کبیسه نیست و روز باید بین 1 تا 28 باشد ، دوباره ارسال کنید", reply_markup= Cancel_markup)
					bot.register_next_step_handler(message, day_check_CE, year, month)
			elif (year % 400 ==0) or (year % 100 != 0) and (year % 4 == 0):
				if not 1 <= int(message.text) <= 29:
					bot.reply_to(message, "سالی که ارسال کردید کبیسه است و تعداد روز باید بین 1 تا 29 باشد ، دوباره ارسال کنید", reply_markup= Cancel_markup)
					bot.register_next_step_handler(message, day_check_CE, year, month)
		else:
			day = int(message.text)
			calculate_date_difference_CE(message, year, month, day)
	except ValueError:
		bot.reply_to(message, "فقط عدد ارسال کنید", reply_markup= Cancel_markup)
		bot.register_next_step_handler(message, day_check_CE, year, month)		

def calculate_date_difference_CE(message, year, month, day):															
	result = Backpack.date_difference_CE(year, month, day)
	bot.send_message(message.chat.id, result, reply_markup= keyboard)

# Related to persian date, when users want to send the year again
@bot.callback_query_handler(func= lambda call: call.data == "sun_back_to_get_year")
def restart_get_year(call):
	bot.clear_step_handler_by_chat_id(call.message.chat.id)
	bot.answer_callback_query(call.id)
	get_year(call.message)
		

# Lottery button run
@bot.message_handler(func= lambda message: message.text == "قرعه کشی⚜️" and message.chat.type == "private")		
def get_lottery_input(message):

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	Cancel_markup.add(Cancel_button)
	
	if not check_membership(message.from_user.id):
		send_membership_message(message.chat.id)
	else:	
		bot.reply_to(message, "اسامی را وارد کنید", reply_markup= Cancel_markup)
		bot.register_next_step_handler(message, do_lottery)

lottery_users = {}

def do_lottery(message):

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel_lottery", style= "danger")
	next_choose_button = types.InlineKeyboardButton("دوباره", callback_data= "do_lottery_again")
	Cancel_markup.add(Cancel_button, next_choose_button)

	user_text = message.text
	lottery_users[message.chat.id] = user_text
	bot_choice = Backpack.lottery(user_text)
	bot.send_message(message.chat.id, f"انتخاب رندوم: {bot_choice}", reply_markup= Cancel_markup)

# Related to lottery, when users want to do lottery again	
@bot.callback_query_handler(func= lambda call: call.data == "do_lottery_again")	
def do_lottery_again(call):
	bot.answer_callback_query(call.id)
	chat_id = call.message.chat.id
	user_text = lottery_users.get(chat_id)
	bot_choice = Backpack.lottery(user_text)

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel_lottery", style= "danger")
	next_choose_button = types.InlineKeyboardButton("دوباره", callback_data= "do_lottery_again")
	Cancel_markup.add(Cancel_button, next_choose_button)

	bot.send_message(chat_id, f"انتخاب رندوم: {bot_choice}", reply_markup= Cancel_markup)

@bot.callback_query_handler(func= lambda call: call.data == "cancel_lottery")
def cancel_lottery(call):
	bot.clear_step_handler_by_chat_id(call.message.chat.id)
	chat_id = call.message.chat.id
	lottery_users.pop(chat_id, None)
	bot.answer_callback_query(call.id)
	bot.send_message(call.message.chat.id, "ابزار مورد نظر را انتخاب کنید", reply_markup= keyboard)	


# Format converter button run
@bot.message_handler(func= lambda message: message.text == "تبدیل فرمت📁" and message.chat.type == "private")
def get_convert_type(message):
	format_converter_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard= True)
	png_jpg_button = types.KeyboardButton("تبدیل PNG به JPG")
	jpg_png_button = types.KeyboardButton("تبدیل JPG به PNG")
	pdf_png_button = types.KeyboardButton("تبدیل PDF به عکس")
	image_pdf_button = types.KeyboardButton("تبدیل عکس به PDF")
	cancel_button = types.KeyboardButton("لغو")
	format_converter_keyboard.add(
		png_jpg_button, jpg_png_button,
		pdf_png_button, image_pdf_button,
		cancel_button,
	)
	if not check_membership(message.from_user.id):
		send_membership_message(message.chat.id)
	else:	
		bot.reply_to(message, "نوع تبدیل را انتخاب کنید", reply_markup= format_converter_keyboard)
		bot.register_next_step_handler(message, check_convert_type)

def check_convert_type(message):
	if message.text not in ["تبدیل PNG به JPG", "تبدیل JPG به PNG", "تبدیل PDF به عکس", "تبدیل عکس به PDF", "لغو"]:
		bot.reply_to(message, "لطفا از منوی زیر انتخاب کنید")
		bot.register_next_step_handler(message, check_convert_type)
	elif message.text == "لغو":		
		bot.clear_step_handler_by_chat_id(message.chat.id)
		bot.send_message(message.chat.id, "ابزار مورد نظر را انتخاب کنید", reply_markup= keyboard)
	else:
		user_demand = message.text
		if user_demand == "تبدیل عکس به PDF":
			get_user_zipped_file(message, user_demand)
		else:	
			get_user_content(message, user_demand)	

def get_user_zipped_file(message, user_demand):
	bot.reply_to(message, "فایل zip تصاویر خود را ارسال کنید. برای راهنمایی بیشتر /help ارسال کنید")
	bot.register_next_step_handler(message, start_converting, user_demand)

def get_user_content(message, user_demand):
		bot.reply_to(message, "از قسمت File محتوای مورد نظر را به شکل Document ارسال کنید")
		bot.register_next_step_handler(message, start_converting, user_demand)

def start_converting(message, user_demand):
	if message.content_type not in ["document"] and message.content_type != "text":
		bot.reply_to(message, "لطفا فایل خود را به شکل Document ارسال کنید")
		get_user_content(message, user_demand)
	elif message.content_type == "text" and message.text == "لغو":
		bot.clear_step_handler_by_chat_id(message.chat.id)
		bot.send_message(message.chat.id, "ابزار مورد نظر را انتخاب کنید", reply_markup= keyboard)	
	elif user_demand == "تبدیل PNG به JPG":		
		file_info = bot.get_file(message.document.file_id)
		user_image_bytes = bot.download_file(file_info.file_path)
		final_image = Backpack.png_jpg(user_image_bytes)
		if final_image is not None:
			bot.send_chat_action(message.chat.id, "upload_document")
			bot.send_document(message.chat.id, final_image, reply_markup= keyboard)
		else:
			bot.send_message(message.chat.id, "خطا در تبدیل فرمت", reply_markup= keyboard)
	elif user_demand == "تبدیل JPG به PNG":
		file_info = bot.get_file(message.document.file_id)
		user_image_bytes = bot.download_file(file_info.file_path)
		final_image = Backpack.jpg_png(user_image_bytes)
		if final_image is not None:
			bot.send_chat_action(message.chat.id, "upload_document")
			bot.send_document(message.chat.id, final_image, reply_markup= keyboard)
		else:
			bot.send_message(message.chat.id, "خطا در تبدیل فرمت", reply_markup= keyboard)
	elif user_demand == "تبدیل PDF به عکس":
		file_info = bot.get_file(message.document.file_id)
		user_pdf = bot.download_file(file_info.file_path)
		images = Backpack.pdf_png(user_pdf)
		if images is not None:
			compressed_images = Backpack.create_zip_file(images)
			if compressed_images is not None:
				bot.send_chat_action(message.chat.id, "upload_document")
				bot.send_document(message.chat.id, compressed_images, reply_markup= keyboard)
			else:
				bot.send_message(message.chat.id, "خطا در فشرده سازی و ارسال فایل")	
		else:
			bot.send_message(message.chat.id, "خطا در تبدیل فرمت", reply_markup= keyboard)
	elif user_demand == "تبدیل عکس به PDF":
		file_info = bot.get_file(message.document.file_id)
		user_zipped_file = bot.download_file(file_info.file_path)
		pdf = Backpack.image_pdf(user_zipped_file)
		if pdf is not None:
			bot.send_chat_action(message.chat.id, "upload_document")
			bot.send_document(message.chat.id, pdf, reply_markup= keyboard)
		else:
			bot.send_message(message.chat.id, "خطا در ساخت PDF", reply_markup= keyboard)				

# Text to speech button run
@bot.message_handler(func= lambda message: message.text == "متن به صوت🎙" and message.chat.type == "private")
def get_speech_gender(message):
	speech_gender_markup = types.InlineKeyboardMarkup(row_width= 2)
	man_button = types.InlineKeyboardButton("مرد", callback_data= "man_speech", style= "primary")
	woman_button = types.InlineKeyboardButton("زن", callback_data= "woman_speech", style= "primary")
	cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	speech_gender_markup.add(
		man_button, woman_button,
		cancel_button,
	)
	if not check_membership(message.from_user.id):
		send_membership_message(message.chat.id)
	else:	
		bot.reply_to(message, "جنسیت صدا را انتخاب کنید", reply_markup= speech_gender_markup)

users_speech_data = {}
@bot.callback_query_handler(func= lambda call: call.data in ["man_speech", "woman_speech"])
def get_text_language(call):
	users_speech_data[call.from_user.id] = [call.data]
	bot.answer_callback_query(call.id)
	bot.delete_message(call.message.chat.id, call.message.message_id)
	speech_language_markup = types.InlineKeyboardMarkup(row_width= 2)
	en_button = types.InlineKeyboardButton("انگلیسی", callback_data= "en_speech", style= "primary")
	fa_button = types.InlineKeyboardButton("فارسی", callback_data= "fa_speech", style= "primary")
	cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	speech_language_markup.add(
		en_button, fa_button,
		cancel_button,
	)

	bot.send_message(call.message.chat.id, "زبان متن مورد نظر را انتخاب کنید", reply_markup= speech_language_markup)

@bot.callback_query_handler(func= lambda call: call.data in ["en_speech", "fa_speech"])
def get_speech_text(call):
	users_speech_data[call.from_user.id].append(call.data)
	bot.answer_callback_query(call.id)
	bot.delete_message(call.message.chat.id, call.message.message_id)
	speech_text(call.message)
	
def speech_text(message):
	bot.send_message(message.chat.id, "حالا متن خود را ارسال کنید")
	bot.register_next_step_handler(message, tts)

def tts(message):
	user_id = int(message.from_user.id)
	text = message.text
	speech_gender = users_speech_data[message.from_user.id][0]
	speech_language = users_speech_data[message.from_user.id][1]
	tts_file = asyncio.run(Backpack.text_to_speech(text, speech_language, speech_gender))
	if tts_file != "مشکلی پیش اومد":
		bot.send_chat_action(message.chat.id, "upload_audio")
		bot.send_audio(message.chat.id, tts_file)
		users_speech_data.pop(user_id, None)
	elif tts_file == "مشکلی پیش اومد":
		bot.send_message(message.chat.id, tts_file)	
		users_speech_data.pop(f"{message.from_user.id}", None)

# User info button run
@bot.message_handler(func= lambda message: message.text == "تلگرام من👤" and message.chat.type == "private")
def send_user_info(message):
	user_first_name = message.from_user.first_name
	user_number_id = message.from_user.id
	user_name = message.from_user.username
	if not check_membership(message.from_user.id):
		send_membership_message(message.chat.id)
	else:	
		bot.reply_to(message, f"🔹Name: {user_first_name}\n🔹User ID: <code>{user_number_id}</code>\n🔹Username: <code>{user_name}</code>", parse_mode= "HTML")


# Inline keyboard button maker run
glass_buttons = {}
@bot.message_handler(func= lambda message: message.text == "دکمه شیشه ای🍷" and message.chat.type == "private")
def get_user_message_inline_button(message):
	user_id = message.from_user.id

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel_inline_button", style= "danger")
	Cancel_markup.add(Cancel_button)
	if not check_membership(message.from_user.id):
		send_membership_message(message.chat.id)
	else:	
		glass_buttons[user_id] = {"message_id": None, "buttons": []}
		bot.reply_to(message, "پست خود را ارسال کنید", reply_markup= Cancel_markup)
		bot.register_next_step_handler(message, preview)


def preview(message):
	user_message_id = message.message_id
	user_id = message.from_user.id
	if user_id in glass_buttons:
		glass_buttons[user_id]["message_id"] = user_message_id
	else:
		glass_buttons[user_id] = {"message_id": None, "buttons": []}
		glass_buttons[user_id]["message_id"] = user_message_id
			
	add_button_markup = types.InlineKeyboardMarkup(row_width= 2)
	add_button = types.InlineKeyboardButton("➕اضافه کردن دکمه", callback_data= "add_inline_button")
	add_button_markup.add(add_button)				
	
	bot.copy_message(message.from_user.id, message.chat.id, message.message_id, reply_markup= add_button_markup)

@bot.callback_query_handler(func= lambda call: call.data == "add_inline_button")
def get_button_link(call):
	user_id = call.from_user.id
	chat_id = call.message.chat.id
	from_chat_id = call.message.chat.id
	message_id = glass_buttons[user_id]["message_id"]

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو فرایند", callback_data= "cancel_inline_button", style= "danger")
	Cancel_markup.add(Cancel_button)

	bot.answer_callback_query(call.id)
	bot.delete_message(call.message.chat.id, call.message.message_id)
	bot.send_message(call.message.chat.id, "لینک خود را ارسال کنید", reply_markup= Cancel_markup)
	bot.register_next_step_handler(call.message, get_button_text, chat_id, from_chat_id, message_id)

def get_button_text(message, chat_id, from_chat_id, message_id):
	button_link = message.text
	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو فرایند", callback_data= "cancel_inline_button", style= "danger")
	Cancel_markup.add(Cancel_button)

	bot.reply_to(message, "متن دکمه را ارسال کنید. برای ظاهر بهتر ، بیشتر از دو کلمه نباشد.", reply_markup= Cancel_markup)
	bot.register_next_step_handler(message, create_button, button_link, chat_id, from_chat_id, message_id)

def create_button(message, button_link, chat_id, from_chat_id, message_id):
	button_text = message.text
	user_id = message.from_user.id
	glass_buttons[user_id]["buttons"].append((button_text, button_link))

	success_markup = types.InlineKeyboardMarkup(row_width= 1)
	send_button = types.InlineKeyboardButton("ارسال پیام به کانال/گروه", callback_data= "send_user_post", style= "success")
	cancel_button = types.InlineKeyboardButton("لغو فرایند", callback_data= "cancel_inline_button", style= "danger")
	success_markup.add(
		send_button, 
		cancel_button,
		)

	prepared_keyboard = create_user_keyboard(user_id)
	if len(glass_buttons[user_id]["buttons"]) < 3:
		prepared_keyboard.add(types.InlineKeyboardButton("➕اضافه کردن دکمه", callback_data= "add_inline_button"))
		bot.copy_message(chat_id, from_chat_id, message_id, reply_markup= prepared_keyboard)
		bot.send_message(message.chat.id, "✅دکمه با موفقیت اضافه شد", reply_markup= success_markup)
	elif len(glass_buttons[user_id]["buttons"]) == 3:
		bot.copy_message(chat_id, from_chat_id, message_id, reply_markup= prepared_keyboard)
		bot.send_message(message.chat.id, "✅دکمه با موفقیت اضافه شد. امکان اضافه کردن بیشتر از سه دکمه برای کاربران معمولی وجود ندارد", reply_markup= success_markup)

def create_user_keyboard(user_id):
	user_keyboard = types.InlineKeyboardMarkup(row_width= 2)
	buttons = []
	for button_text, button_link in glass_buttons[user_id]["buttons"]:
		buttons.append(types.InlineKeyboardButton(text= button_text, url= button_link))
	user_keyboard.add(*buttons)	
	return user_keyboard

@bot.callback_query_handler(func= lambda call: call.data == "send_user_post")
def get_channelorgroup_id(call):
	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو فرایند", callback_data= "cancel_inline_button", style= "danger")
	Cancel_markup.add(Cancel_button)
	if call.from_user.id in glass_buttons:
		bot.answer_callback_query(call.id)
		bot.send_message(call.message.chat.id, "آیدی کانال/گروه مورد نظر را ارسال کنید. ربات باید در آن عضو و دسترسی های لازم را داشته باشد", reply_markup= Cancel_markup)
		bot.register_next_step_handler(call.message, check_bot_membership)
	else:
		bot.answer_callback_query(call.id)
		bot.send_message(call.message.chat.id, "پیام شما حذف شده است. لطفا یک پیام جدید ارسال کنید", reply_markup= Cancel_markup)
		bot.register_next_step_handler(call.message, preview)	

def check_bot_membership(message):

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو فرایند", callback_data= "cancel_inline_button", style= "danger")
	Cancel_markup.add(Cancel_button)
	
	chat_id = message.text
	bot_id = bot.get_me().id
	try:
		membership = bot.get_chat_member(chat_id, bot_id)
		chat = bot.get_chat(chat_id)
		check_bot_access(message, membership, chat, chat_id)	
	except Exception:
		bot.send_message(message.chat.id, "❌آیدی وجود ندارد و یا ربات عضو این کانال/گروه نیست ، ربات را اضافه کرده و دوباره آیدی را ارسال کنید", reply_markup= Cancel_markup)	
		bot.register_next_step_handler(message, check_bot_membership)

def check_bot_access(message, membership, chat, chat_id):
	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو فرایند", callback_data= "cancel_inline_button", style= "danger")
	Cancel_markup.add(Cancel_button)

	if membership.status in ["left", "kicked"]:
		bot.send_message(message.chat.id, "❌ربات در کانال یا گروه ارسال شده عضو نیست ، ربات را اضافه کرده و دوباره آیدی کانال/گروه را ارسال کنید", reply_markup= Cancel_markup)
		bot.register_next_step_handler(message, check_bot_membership)
	elif chat.type == "channel":
		if membership.status != "administrator":
			bot.send_message(message.chat.id, "❌ربات در کانال ارسال شده ادمین نیست ، دسترسی لازم را بدید و آیدی را دوباره ارسال کنید", reply_markup= Cancel_markup)
			bot.register_next_step_handler(message, check_bot_membership)
		else:
			send_post(message, chat_id)
	elif chat.type in ["group", "supergroup"]:
		send_post(message, chat_id)

def send_post(message, chat_id):
	user_id = message.from_user.id

	send_post_keyboard = types.InlineKeyboardMarkup(row_width= 1)
	send_another_chat = types.InlineKeyboardButton("ارسال به چت دیگر", callback_data= "send_ready_message_agian", style= "success")
	finished_button = types.InlineKeyboardButton("تمام", callback_data= "cancel_inline_button", style= "danger")
	send_post_keyboard.add(
		send_another_chat,
		finished_button,
	)

	prepared_keyboard = create_user_keyboard(user_id)
	try:
		bot.copy_message(chat_id, user_id, glass_buttons[user_id]["message_id"], reply_markup= prepared_keyboard)
		bot.send_message(message.chat.id, "✅پیام با موفقیت ارسال شد", reply_markup= send_post_keyboard)
	except:
		bot.send_message(message.chat.id, "❌امکان ارسال به این چت وجود ندارد", reply_markup= send_post_keyboard)	

@bot.callback_query_handler(func= lambda call: call.data == "cancel_inline_button")
def cancel_sending_message(call):
		bot.answer_callback_query(call.id)
		glass_buttons.pop(call.from_user.id, None)
		bot.clear_step_handler_by_chat_id(call.message.chat.id)
		bot.send_message(call.message.chat.id, "ابزار مورد نظر را انتخاب کنید", reply_markup= keyboard)

@bot.callback_query_handler(func= lambda call: call.data == "send_ready_message_agian")
def send_ready_message_again(call):

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو فرایند", callback_data= "cancel_inline_button", style= "danger")
	Cancel_markup.add(Cancel_button)
	if call.from_user.id in glass_buttons:
		bot.answer_callback_query(call.id)
		bot.send_message(call.message.chat.id, "آیدی کانال/گروه مورد نظر را ارسال کنید. ربات باید در آن عضو و دسترسی های لازم را داشته باشد", reply_markup= Cancel_markup)
		bot.register_next_step_handler(call.message, check_bot_membership)
	else:
		bot.answer_callback_query(call.id)
		bot.send_message(call.message.chat.id, "پیام شما حذف شده است. لطفا یک پیام جدید ارسال کنید", reply_markup= Cancel_markup)
		bot.register_next_step_handler(call.message, preview)					

@bot.message_handler(func= lambda message: message.text == "پریمیوم" and message.chat.type == "private")
def buy_premium(message):
	pass

# Group message handler zone
# Here, we handle messages those have sent by group users
@bot.message_handler(func= lambda message: message.chat.type in ["group", "supergroup"] and message.text in Backpack.currencies or message.text in ["تتر", "دلار", "یورو", "طلا"])
def group_currency_prices(message):
	currency_name = message.text
	price = Backpack.APIprices(currency_name)
	bot.send_message(message.chat.id, price)


# When users send irrelevant messages
@bot.message_handler(func=lambda message: True and message.chat.type == "private")
def echo_all(message):
	bot.reply_to(message, "از منوی زیر ابزار مورد نظر را انتخاب کنید\nبرای راهنمایی /help را ارسال کنید", reply_markup= keyboard)

# Running the bot
bot.infinity_polling()