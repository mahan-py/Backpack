# Requirements

import webbrowser
from bs4 import BeautifulSoup
import requests
from abc import ABC, abstractmethod
import string
import random
from datetime import date
from deep_translator import GoogleTranslator
import jdatetime
from PIL import Image
import pathlib
import pymupdf
from io import BytesIO

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

# Currency price tool

def prices(currency_name):

    if currency_name == "دلار":
        try:
            site = requests.get("https://www.tgju.org/profile/price_dollar_rl")
            soup = BeautifulSoup(site.text, "html.parser")
            price = soup.find("span", attrs={"data-col": "info.last_trade.PDrCotVal"}).text
            return (f"قیمت دلار {price} ریال")
        except:
            return ("مشکلی پیش آمد ، اتصال به اینترنت را بررسی کنید")        
    elif currency_name == "یورو":
        try:
            site = requests.get("https://www.tgju.org/profile/price_eur")
            soup = BeautifulSoup(site.text, "html.parser")
            price = soup.find("span", attrs={"data-col": "info.last_trade.PDrCotVal"}).text
            return (f"قیمت یورو {price} ریال")
        except:
            return ("مشکلی پیش آمد ، اتصال به اینترنت را بررسی کنید")    
    elif currency_name == "طلا":
        try:
            site = requests.get("https://www.tgju.org/profile/geram18")
            soup = BeautifulSoup(site.text, "html.parser")
            price = soup.find("span", attrs={"data-col": "info.last_trade.PDrCotVal"}).text
            return (f"قیمت طلا {price} ریال")
        except:
            return ("مشکلی پیش آمد ، اتصال به اینترنت را بررسی کنید")    
    elif currency_name == "بیت کوین":
        try:
            site = requests.get("https://nobitex.ir/buy/btc/")
            soup = BeautifulSoup(site.text, "html.parser")
            price1 = soup.find("span", attrs={"class": "text-headline-large"}).text
            price2 = soup.find("span", attrs={"class": "text-body-large"}).text
            return (f"قیمت بیت کوین {price2} تومان\nبرابر با {price1} تتر")
        except:
            return ("مشکلی پیش آمد ، اتصال به اینترنت را بررسی کنید")
    elif currency_name == "تتر":
        try:
            site = requests.get("https://nobitex.ir/price/usdt/")
            soup = BeautifulSoup(site.text, "html.parser")
            price = soup.find("span", attrs={"class": "text-body-large"}).text
            return (f"قیمت تتر {price} تومان")
        except:
            return ("مشکلی پیش آمد ، اتصال به اینترنت را بررسی کنید")
    elif currency_name == "گرام":
        try:
            site = requests.get("https://nobitex.ir/buy/gram/")
            soup = BeautifulSoup(site.text, "html.parser")
            price1 = soup.find("span", attrs={"class": "text-headline-large"}).text
            price2 = soup.find("span", attrs={"class": "text-body-large"}).text
            return (f"قیمت گرام {price2} تومان\nبرابر با {price1} تتر")
        except:
            return ("مشکلی پیش آمد ، اتصال به اینترنت را بررسی کنید")
    elif currency_name == "سولانا":
        try:
            site = requests.get("https://nobitex.ir/price/sol/")
            soup = BeautifulSoup(site.text, "html.parser")
            price1 = soup.find("span", attrs={"class": "text-headline-large"}).text
            price2 = soup.find("span", attrs={"class": "text-body-large"}).text
            return (f"قیمت سولانا {price2} تومان\nبرابر با {price1} تتر")
        except:
            return ("مشکلی پیش آمد ، اتصال به اینترنت را بررسی کنید")
    elif currency_name == "اتریوم":
        try:
            site = requests.get("https://nobitex.ir/buy/eth/")
            soup = BeautifulSoup(site.text, "html.parser")
            price1 = soup.find("span", attrs={"class": "text-headline-large"}).text
            price2 = soup.find("span", attrs={"class": "text-body-large"}).text
            return (f"قیمت اتریوم {price2} تومان\nبرابر با {price1} تتر")
        except:
            return ("مشکلی پیش آمد ، اتصال به اینترنت را بررسی کنید")
    elif currency_name.upper() == "DOGECOIN" or currency_name == "دوج کوین":
        try:
            site = requests.get("https://nobitex.ir/buy/doge/")
            soup = BeautifulSoup(site.text, "html.parser")
            price1 = soup.find("span", attrs={"class": "text-headline-large"}).text
            price2 = soup.find("span", attrs={"class": "text-body-large"}).text
            return (f"قیمت دوج کوین {price2} تومان\nبرابر با {price1} تتر")
        except:
            return ("مشکلی پیش آمد ، اتصال به اینترنت را بررسی کنید")
    elif currency_name.upper() == "SHIBA" or currency_name == "شیبا":
        try:
            site = requests.get("https://nobitex.ir/buy/1k_shib/")
            soup = BeautifulSoup(site.text, "html.parser")
            price1 = soup.find("span", attrs={"class": "text-headline-large"}).text
            price2 = soup.find("span", attrs={"class": "text-body-large"}).text
            return (f"قیمت شیبا {price2} تومان\nبرابر با {price1} تتر")
        except:
            return ("مشکلی پیش آمد ، اتصال به اینترنت را بررسی کنید")
    elif currency_name == "ریپل":
        try:
            site = requests.get("https://nobitex.ir/buy/xrp/")
            soup = BeautifulSoup(site.text, "html.parser")
            price1 = soup.find("span", attrs={"class": "text-headline-large"}).text
            price2 = soup.find("span", attrs={"class": "text-body-large"}).text
            return (f"قیمت ریپل {price2} تومان\nبرابر با {price1} تتر")
        except:
            return ("مشکلی پیش آمد ، اتصال به اینترنت را بررسی کنید")                                                    
    else:
        return ("اطلاعاتی درمورد این ارز ندارم")            
    
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