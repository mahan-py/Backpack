# Requirements

import webbrowser
from bs4 import BeautifulSoup
import requests
from abc import ABC, abstractmethod
import string
import random
from datetime import date
import datetime
import jdatetime
from PIL import Image
import pathlib
import pymupdf
from io import BytesIO
import zipfile
from natsort import natsorted
import edge_tts
import asyncio
from decimal import Decimal
import telebot
from telebot import types

# Average tool
 
def takes_average(numbers):   
        count = 0
        correct_numbers = [float(e) for e in numbers.split()]
        for i in correct_numbers:
            count += i
            average = count / len(correct_numbers)   
        return (f"{average:.3f}")

# Calculating the BMI tool

def bmi(weight, height):
    with open("BMImessage.txt", "r", encoding= "utf-8") as file1:
        bmi_message = file1.read()
    bmi = weight / (height ** 2)
    
    if bmi < 18.5:
        return (f"BMI = {bmi:.3f}\nکمبود وزن\n{bmi_message}")
    elif 18.5 <= bmi <= 24.9:
        return (f"BMI = {bmi:.3f}\nوزن نرمال\n{bmi_message}")
    elif 25 <= bmi <= 29.9:
        return (f"BMI = {bmi:.3f}\nاضافه وزن\n{bmi_message}")
    elif 30 <= bmi <= 34.9:
        return (f"BMI = {bmi:.3f}\nچاقی درجه یک\n{bmi_message}")
    elif 35 <= bmi <= 39.9:
        return (f"BMI = {bmi:.3f}\nچاقی درجه دو\n{bmi_message}")
    elif 40 <= bmi:
        return (f"BMI = {bmi:.3f}\nچاقی درجه سه\n{bmi_message}")

# Currency price tool (with API)

nobitex_data = None
nobitex_last_request_minute = -1
def get_market_data():
    global nobitex_last_request_minute, nobitex_data
    current_minute = (datetime.datetime.today().time().minute)
    if current_minute != nobitex_last_request_minute:
        url = "https://apiv2.nobitex.ir/market/stats"

        payload = {}
        headers = {
        'Accept': 'application/json'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        nobitex_data = response.json()
        nobitex_last_request_minute = current_minute
        return nobitex_data
    else:
        return nobitex_data     

currencies = {
    "گرام": "gram", "بیت کوین": "btc", "اتریوم": "eth", "ریپل": "xrp", "سولانا": "sol", "دوج کوین": "doge", "نات کوین": "not", "داگز": "dogs", "شیبا": "1k_shib", "کاردانو": "ada",
    "سونیک": "s", "گراف": "grt", "سویی": "sui", "ترون": "trx", "سیناپس": "syn", "تزوس": "xtz", "دش": "dash", "زن": "zen", "فایل کوین": "fil", "دای": "dai", "بیبی دوج": "1b_babydoge",
}
def APIprices(currency_name):
    data = get_market_data()
    if currency_name in currencies:
        try:
            best_buy = Decimal(data["stats"][f"{currencies[currency_name]}-rls"]["bestBuy"][:-1])
            best_sell = Decimal(data["stats"][f"{currencies[currency_name]}-rls"]["bestSell"][:-1])
            change_percent = data["stats"][f"{currencies[currency_name]}-rls"]["dayChange"]
            t_best_buy = data["stats"][f"{currencies[currency_name]}-usdt"]["bestBuy"]
            t_best_sell = data["stats"][f"{currencies[currency_name]}-usdt"]["bestSell"]
            t_change_percent = data["stats"][f"{currencies[currency_name]}-usdt"]["dayChange"]

            ready_rich_message = types.InputRichMessage(
                html=f"""
                <h3>جدول قیمت 💰</h3> 
                <table bordered>
                    <tr>
                        <th>{currency_name}</th>
                        <th>تومان</th>
                        <th>تتر</th>
                    </tr>
                    <tr>
                        <td>خرید</td>
                        <td>{best_buy:,}</td>
                        <td>{t_best_buy}</td>
                    </tr>
                    <tr>
                        <td>فروش</td>
                        <td>{best_sell:,}</td>
                        <td>{t_best_sell}</td>
                    </tr>
                    <tr>
                        <td>تغییرات</td>
                        <td>{change_percent}</td>
                        <td>{t_change_percent}</td>
                    </tr>
                </table>
                <tg-button-row align="center">
                    <tg-button type="callback_data" data="cancel" style="danger">برگشت به منوی اصلی</tg-button>
                </tg-button-row>            
                """,
                is_rtl= True
            )

            return ready_rich_message                           
        
        except:
            return None

    elif currency_name == "تتر":
        try:
            best_buy = int(data["stats"]["usdt-rls"]["bestBuy"][:-1])
            best_sell = int(data["stats"]["usdt-rls"]["bestSell"][:-1])
            change_percent = data["stats"]["usdt-rls"]["dayChange"]

            ready_rich_message = types.InputRichMessage(
                html=f"""
                <h3>جدول قیمت 💰</h3> 
                <table bordered>
                    <tr>
                        <th>{currency_name}</th>
                        <th>تومان</th>
                    </tr>
                    <tr>
                        <td>خرید</td>
                        <td>{best_buy:,}</td>
                    </tr>
                    <tr>
                        <td>فروش</td>
                        <td>{best_sell:,}</td>
                    </tr>
                    <tr>
                        <td>تغییرات</td>
                        <td>{change_percent}</td>
                    </tr>
                </table>
                <tg-button-row align="center">
                    <tg-button type="callback_data" data="cancel" style="danger">برگشت به منوی اصلی</tg-button>
                </tg-button-row>            
                """,
                is_rtl= True
            )

            return ready_rich_message                           
        
        except:
            return None
    
    elif currency_name == "دلار":
        try:
            site = requests.get("https://www.tgju.org/profile/price_dollar_rl")
            soup = BeautifulSoup(site.text, "html.parser")
            rls_price = soup.find("span", attrs={"data-col": "info.last_trade.PDrCotVal"}).text
            toman_price = int(rls_price.replace(",", "")) // 10

            ready_rich_message = types.InputRichMessage(
                html=f"""
                <h3>جدول قیمت 💰</h3> 
                <table bordered>
                    <tr>
                        <th>{currency_name}</th>
                        <th>تومان</th>
                    </tr>
                    <tr>
                        <td>خرید</td>
                        <td>{toman_price:,}</td>
                    </tr>
                </table>
                <tg-button-row align="center">
                    <tg-button type="callback_data" data="cancel" style="danger">برگشت به منوی اصلی</tg-button>
                </tg-button-row>            
                """,
                is_rtl= True
            )

            return ready_rich_message
        
        except Exception as e:
            print(e)
            return None
    
    elif currency_name == "طلا":
        try:
            site = requests.get("https://www.tgju.org/profile/geram18")
            soup = BeautifulSoup(site.text, "html.parser")
            rls_price = soup.find("span", attrs={"data-col": "info.last_trade.PDrCotVal"}).text
            toman_price = int(rls_price.replace(",", "")) // 10

            ready_rich_message = types.InputRichMessage(
                html=f"""
                <h3>جدول قیمت 💰</h3> 
                <table bordered>
                    <tr>
                        <th>{currency_name}</th>
                        <th>تومان</th>
                    </tr>
                    <tr>
                        <td>خرید</td>
                        <td>{toman_price:,}</td>
                    </tr>
                </table>
                <tg-button-row align="center">
                    <tg-button type="callback_data" data="cancel" style="danger">برگشت به منوی اصلی</tg-button>
                </tg-button-row>            
                """,
                is_rtl= True
            )

            return ready_rich_message
        
        except:
            return None

    elif currency_name == "یورو":
        try:
            site = requests.get("https://www.tgju.org/profile/price_eur")
            soup = BeautifulSoup(site.text, "html.parser")
            rls_price = soup.find("span", attrs={"data-col": "info.last_trade.PDrCotVal"}).text
            toman_price = int(rls_price.replace(",", "")) // 10

            ready_rich_message = types.InputRichMessage(
                html=f"""
                <h3>جدول قیمت 💰</h3> 
                <table bordered>
                    <tr>
                        <th>{currency_name}</th>
                        <th>تومان</th>
                    </tr>
                    <tr>
                        <td>خرید</td>
                        <td>{toman_price:,}</td>
                    </tr>
                </table>
                <tg-button-row align="center">
                    <tg-button type="callback_data" data="cancel" style="danger">برگشت به منوی اصلی</tg-button>
                </tg-button-row>            
                """,
                is_rtl= True
            )

            return ready_rich_message 
        
        except:
            return None                                                                                  
    
    else:
        return "اطلاعاتی درمورد این ارز ندارم"

# Password generator tool

class PasswordGeneratorAbstract(ABC):
    @abstractmethod
    def generate_password(self, length = 10):
        pass

class NumbericPasswordGenerator(PasswordGeneratorAbstract):
    numbers = string.digits
    def generate_password(self, length = 10):
        return "".join(str(random.choice(self.numbers)) for _ in range(length))

class LetterPasswordGenerator(PasswordGeneratorAbstract):
    letters = string.ascii_letters
    def generate_password(self, length = 10):
        return "".join(str(random.choice(self.letters)) for _ in range(length))

class MixedPasswordGenerator(PasswordGeneratorAbstract):
    numbers_letters = string.ascii_letters + string.digits
    def generate_password(self, length = 10):
        return "".join(str(random.choice(self.numbers_letters)) for _ in range(length))

# Date difference calculator tool

def date_difference_CE(year, month, day):
    
    now = date.today()
    present_year = now.year
    present_month = now.month
    present_day = now.day
    
    day_difference = present_day - day
    if day_difference < 0:
        present_month -= 1
        if present_month == 0:
            present_month = 12
            present_year -= 1
        if present_month in [1, 3, 5, 7, 8, 10, 12]:
            present_day += 31
            day_difference = present_day - day
        elif present_month in [4, 6, 9, 11]:
            present_day += 30
            day_difference = present_day - day
        elif present_month == 2:
            if not (present_year % 4 ==0) and (present_year % 100 != 0) or (present_year % 400 == 0):
                present_day += 28
                day_difference = present_day - day
            else:
                present_day += 29
                day_difference = present_day - day            

    month_difference = present_month - month
    if month_difference < 0:
        present_year -= 1
        present_month += 12
        month_difference = present_month - month    

    year_difference = present_year - year

    return (f"اختلاف تاریخ: {year_difference} سال و {month_difference} ماه و {day_difference} روز")



def shamsi_date_difference(year, month, day):
    
    now = jdatetime.date.today()
    present_year = now.year
    present_month = now.month
    present_day = now.day


    day_difference = present_day - day
    if day_difference < 0:
        present_month -= 1
        if present_month == 0:
            present_month = 12
            present_year -= 1
        if present_month in [1, 2, 3, 4, 5, 6]:
            present_day += 31
            day_difference = present_day - day
        elif present_month in [7, 8, 9, 10, 11]:
            present_day += 30
            day_difference = present_day - day
        elif present_month == 12:
            if not (present_year % 4 ==0) and (present_year % 100 != 0) or (present_year % 400 == 0):
                present_day += 29
                day_difference = present_day - day
            else:
                present_day += 30
                day_difference = present_day - day            

    month_difference = present_month - month
    if month_difference < 0:
        present_year -= 1
        present_month += 12
        month_difference = present_month - month    

    year_difference = present_year - year
    return (f"اختلاف تاریخ: {year_difference} سال و {month_difference} ماه و {day_difference} روز")    

# Translator tool    

def translator(user_text, user_target_language):
    text = user_text
    target_language = user_target_language
    translator = GoogleTranslator(source='auto', target='fa')
    
    if target_language == "انگلیسی":
        translator.target = "en"
    elif target_language == "عربی":
        translator.target = "ar"
    elif target_language == "فرانسوی":
        translator.target = "fr"
    elif target_language == "چینی":
        translator.target = "zh-CN"
    elif target_language == "آلمانی":
        translator.target = "de"
    elif target_language == "ترکی":
        translator.target = "tr"
    elif target_language == "روسی":
        translator.target = "ru"
    elif target_language == "اسپانیایی":
        translator.target = "es"
    elif target_language == "فارسی":
        translator.target = "fa"                
    else:
        translator.target = target_language
                            
    try:
        result = translator.translate(text= text)
        return result
    except Exception:
        return "مشکلی پیش آمده است"

# Lottery tool

def lottery(user_text):
    user_input = user_text
    spliter = user_input.split(" ")
    dish = []
    for item in spliter:
        if item.isalpha() == True:
            dish.append(item)
        elif item.isdigit() == True:
            dish.append(item)
        elif item.isalnum() == True:
            dish.append(item)        

    choice = random.choice(dish)
    return choice
    
# Format converter tool

def png_jpg(user_image_bytes):
    try:
        img = Image.open(BytesIO(user_image_bytes))
        output = BytesIO()
        img = img.convert("RGB")
        img.save(output, format="JPEG")
        output.seek(0)
        output.name = "converted.jpg"
        return output
    except:
        return None                        

def jpg_png(user_image_bytes):
    try:
        img = Image.open(BytesIO(user_image_bytes))
        output = BytesIO()
        img.save(output, format="PNG")
        output.seek(0)
        output.name = "converted.png"
        return output
    except:
        return None

def pdf_png(user_pdf):
   try: 
       pdf = pymupdf.open(stream= user_pdf, filetype= "pdf")
       images = []
       for page in pdf:
           image = page.get_pixmap(dpi= 150)
           images.append(image.tobytes("png"))
       return images
   except:
        return None

def image_pdf(user_zipped_file):
    try:
        user_zipped_file = BytesIO(user_zipped_file)
        images = []
        with zipfile.ZipFile(user_zipped_file, "r") as zipped_file:
            file_names = natsorted(zipped_file.namelist())
            for file_name in file_names:
                if file_name.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
                    image_data = zipped_file.read(file_name)
                    image_file = BytesIO(image_data)
                    img = Image.open(image_file)
                    img.load()
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    images.append(img)        
        
        pdf_file = BytesIO()
        images[0].save(pdf_file, format= "PDF", save_all= True, append_images = images[1:])
        pdf_file.name = "Converted.pdf"
        pdf_file.seek(0)
        return pdf_file
    except:
        return None    


def create_zip_file(images):
    try:
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for index, image in enumerate(images, start= 1):
                zip_file.writestr(f"page{index}.png", image)

        zip_buffer.seek(0)
        zip_buffer.name = "Converted.zip"
        return zip_buffer
    except:
        return None

# Text to speech tool

async def text_to_speech(text, language, gender):
    try:
        audio = BytesIO()
        if gender == "man_speech":
            if language == "en_speech":
                tts = edge_tts.Communicate(text, "en-US-GuyNeural")
            elif language == "fa_speech":
                tts = edge_tts.Communicate(text, "fa-IR-FaridNeural")
        elif gender == "woman_speech":
            if language == "en_speech":
                tts = edge_tts.Communicate(text, "en-US-AriaNeural")
            elif language == "fa_speech":
                tts = edge_tts.Communicate(text, "fa-IR-DilaraNeural")

        async for chunk in tts.stream():
            if chunk["type"] == "audio":
                audio.write(chunk["data"])
        audio.seek(0)
        audio.name = "voice.mp3"
        return audio
    except:
        return "مشکلی پیش اومد"                                            