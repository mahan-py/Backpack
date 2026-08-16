import telebot
from telebot import types
from Backpack import takes_average
from Backpack import bmi
from Backpack import prices
from Backpack import PasswordGeneratorAbstract, NumbericPasswordGenerator, LetterPasswordGenerator, MixedPasswordGenerator
from Backpack import translator
from Backpack import lottery
from Backpack import shamsi_date_difference

# Some messages were too long so i created txt files and wrote them there
with open("startmessage.txt", "r", encoding= "utf-8") as file:
    start_message = file.read()

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
		send_welcome(call.message)
	else:
		bot.answer_callback_query(call.id, "هنوز عضو نیستید!", show_alert= True)			


# Main keyboard buttons
keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
average_button = types.KeyboardButton("میانگین")
bmi_button = types.KeyboardButton("BMI")
currency_button = types.KeyboardButton("قیمت ارز")
password_button = types.KeyboardButton("تولید رمز")
date_difference_button = types.KeyboardButton("اختلاف تاریخ")
translate_button = types.KeyboardButton("ترجمه")
lottery_button = types.KeyboardButton("قرعه کشی")
keyboard.add(
	average_button, bmi_button,
	currency_button, password_button,
	date_difference_button, translate_button,
	lottery_button
)

# Starting the bot for the first time or reaction to /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
	if not check_membership(message.from_user.id):
		send_membership_message(message.chat.id)
	else:	
		bot.send_message(message.chat.id, start_message, reply_markup= keyboard)

# Sends a general guide to help users
@bot.message_handler(commands=['help'])
def send_help(message):
	bot.reply_to(message, help_message)
	send_welcome(message)		

# Average button run
@bot.message_handler(func= lambda message: message.text == "میانگین")
def average_tool(message):
	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	Cancel_markup.add(Cancel_button)
	if not check_membership(message.from_user.id):
		send_membership_message(message.chat.id)
	else:	
		bot.reply_to(message, "لطفا اعداد را به انگلیسی و بدون علامت ریاضی و یا حروف ارسال کنید", reply_markup= Cancel_markup)
		bot.register_next_step_handler(message, get_numbers)

def get_numbers(message):
	try:
		numbers = message.text
		average = takes_average(numbers)
		bot.send_message(message.chat.id, average)
	except:
		bot.send_message(message.chat.id, "مشکلی پیش اومد")	

# BMI button run
@bot.message_handler(func= lambda message: message.text == "BMI")
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
			user_BMI = bmi(weight, height)

			bmi_information_sources = types.InlineKeyboardMarkup()
			source = types.InlineKeyboardButton("اطلاعات بیشتر", url= "https://fa.wikipedia.org/wiki/%D8%B4%D8%A7%D8%AE%D8%B5_%D8%AA%D9%88%D8%AF%D9%87_%D8%A8%D8%AF%D9%86%DB%8C")
			bmi_information_sources.add(source)

			bot.send_message(message.chat.id, user_BMI, reply_markup= bmi_information_sources)	
	except ValueError:
		bot.reply_to(message, "لطفا عدد ارسال کنید")
		bot.register_next_step_handler(message, get_height, weight)

# Prices button run
@bot.message_handler(func= lambda message: message.text == "قیمت ارز")
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
		bot.reply_to(message, "ارز مورد نظر را وارد کنید", reply_markup= currency_keyboard)
		bot.send_message(message.chat.id, "اگر ارز مورد نظر در لیست نیست ، کافیه اسم کامل آن را وارد کنید", reply_markup= Cancel_markup)
		bot.register_next_step_handler(message, find_price)

def find_price(message):

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("برگشت به منوی اصلی", callback_data= "cancel", style= "danger")
	Cancel_markup.add(Cancel_button)

	currency_name = message.text
	price = prices(currency_name)
	bot.reply_to(message, price, reply_markup= Cancel_markup)
	bot.register_next_step_handler(message, find_price)

# Password generator
@bot.message_handler(func= lambda message: message.text == "تولید رمز")
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
		user_password = NumbericPasswordGenerator()
		result = user_password.generate_password(length= length)
		bot.send_message(message.chat.id, result, reply_markup= keyboard)
	elif password_type == "فقط شامل حروف":
		user_password = LetterPasswordGenerator()
		result = user_password.generate_password(length= length)
		bot.send_message(message.chat.id, result, reply_markup= keyboard)
	elif password_type == "ترکیبی":
		user_password = MixedPasswordGenerator()
		result = user_password.generate_password(length= length)
		bot.send_message(message.chat.id, result, reply_markup= keyboard)		

# When users want to choose password type again
@bot.callback_query_handler(func= lambda call: call.data == "check_type_back")
def restart_get_password_type(call):
	bot.clear_step_handler_by_chat_id(call.message.chat.id)
	bot.answer_callback_query(call.id)
	get_password_type(call.message)

# Date difference button run
@bot.message_handler(func= lambda message: message.text == "اختلاف تاریخ")
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
	result = shamsi_date_difference(year, month, day)
	bot.send_message(message.chat.id, result, reply_markup= keyboard)

# CE date requirements related to next function
import datetime
from Backpack import date_difference_CE
now_CE = datetime.date.today()
present_CE_year = now_CE.year
present_CE_month = now_CE.month
present_CE_day = now_CE.day

# When users choose Persian date type
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
	result = date_difference_CE(year, month, day)
	bot.send_message(message.chat.id, result, reply_markup= keyboard)

# Related to persian date, when users want to send the year again
@bot.callback_query_handler(func= lambda call: call.data == "sun_back_to_get_year")
def restart_get_year(call):
	bot.clear_step_handler_by_chat_id(call.message.chat.id)
	bot.answer_callback_query(call.id)
	get_year(call.message)
		

# Translater button run
@bot.message_handler(func= lambda message: message.text == "ترجمه")
def get_user_text(message):
	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	Cancel_markup.add(Cancel_button)
	
	if not check_membership(message.from_user.id):
		send_membership_message(message.chat.id)
	else:	
		bot.reply_to(message, "متن خود را ارسال کنید", reply_markup= Cancel_markup)
		bot.register_next_step_handler(message, translate_text)
def translate_text(message):
	target_language_keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard= True)
	language_button1 = types.KeyboardButton("فارسی")
	language_button2 = types.KeyboardButton("انگلیسی")
	language_button3 = types.KeyboardButton("چینی")
	language_button4 = types.KeyboardButton("فرانسوی")
	language_button5 = types.KeyboardButton("اسپانیایی")
	language_button6 = types.KeyboardButton("آلمانی")
	language_button7 = types.KeyboardButton("روسی")
	language_button8 = types.KeyboardButton("ترکی")
	language_button9 = types.KeyboardButton("عربی")
	target_language_keyboard.add(
		language_button1, language_button2, language_button3,
		language_button4, language_button5, language_button6,
		language_button7, language_button8, language_button9,
	)

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	back_button = types.InlineKeyboardButton("مرحله قبل", callback_data= "translate_text_back", style= "primary")
	Cancel_markup.add(Cancel_button, back_button)

	user_text = message.text
	bot.reply_to(message, "از منوی زیر ، زبان هدف را انخاب کنید", reply_markup= target_language_keyboard)
	bot.send_message(message.chat.id, "میتوانید به مرحله قبل برگردید و یا فرایند را لغو کنید", reply_markup= Cancel_markup)
	bot.register_next_step_handler(message, check_target_language, user_text)
def check_target_language(message, user_text):

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	back_button = types.InlineKeyboardButton("مرحله قبل", callback_data= "translate_text_back", style= "primary")
	Cancel_markup.add(Cancel_button, back_button)

	if message.text not in ["انگلیسی", "فارسی", "چینی", "فرانسوی", "اسپانیایی", "آلمانی", "روسی", "ترکی", "عربی"]:
		bot.reply_to(message, "زبان یافت نشد ، دوباره وارد کنید", reply_markup= Cancel_markup)
		bot.register_next_step_handler(message, check_target_language, user_text)
	else:
		user_target_language = message.text
		result = translator(user_text, user_target_language)
		bot.send_message(message.chat.id, result, reply_markup= keyboard)		

# Related to translator tool, when users want to send the text again
@bot.callback_query_handler(func= lambda call: call.data == "translate_text_back")
def restart_get_user_text(call):
	bot.clear_step_handler_by_chat_id(call.message.chat.id)
	bot.answer_callback_query(call.id)
	get_user_text(call.message)

# Lottery button run
@bot.message_handler(func= lambda message: message.text == "قرعه کشی")		
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
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	next_choose_button = types.InlineKeyboardButton("دوباره", callback_data= "do_lottery_again")
	Cancel_markup.add(Cancel_button, next_choose_button)

	user_text = message.text
	lottery_users[message.chat.id] = user_text
	bot_choice = lottery(user_text)
	bot.send_message(message.chat.id, bot_choice, reply_markup= Cancel_markup)
	bot.register_next_step_handler(user_text, do_lottery_again)

# Related to lottery, when users want to do lottery again	
@bot.callback_query_handler(func= lambda call: call.data == "do_lottery_again")	
def do_lottery_again(call):
	bot.answer_callback_query(call.id)
	chat_id = call.message.chat.id
	user_text = lottery_users.get(chat_id)
	bot_choice = lottery(user_text)

	Cancel_markup = types.InlineKeyboardMarkup()
	Cancel_button = types.InlineKeyboardButton("لغو", callback_data= "cancel", style= "danger")
	next_choose_button = types.InlineKeyboardButton("دوباره", callback_data= "do_lottery_again")
	Cancel_markup.add(Cancel_button, next_choose_button)

	bot.send_message(chat_id, bot_choice, reply_markup= Cancel_markup)
	

# When users send irrelevant messages
@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, start_message, reply_markup= keyboard)

# Running the bot
bot.infinity_polling()