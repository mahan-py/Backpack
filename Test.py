import unittest
from unittest.mock import patch
from datetime import date as real_date
from jdatetime import date as real_persian_date
from Backpack import takes_average, bmi, prices, date_difference_CE, shamsi_date_difference, translator, lottery

class test_average_tool(unittest.TestCase):
    def test1(self):
        numbers = ("12 13.5 14 15.5 16")
        self.assertEqual(takes_average(numbers), '14.200')
    def test2(self):
        numbers = ("1 2 3 0 4")
        self.assertEqual(takes_average(numbers), '2.000')

class test_bmi_tool(unittest.TestCase):
    def test1(self):
        weight = 55
        height = 1.75
        self.assertIn("BMI = 17.959", bmi(weight, height))        
        self.assertIn("کمبود وزن", bmi(weight, height))
    def test2(self):
        weight = 62
        height = 1.75
        self.assertIn("BMI = 20.245", bmi(weight, height))        
        self.assertIn("وزن نرمال", bmi(weight, height))
    def test3(self):
        weight = 78
        height = 1.75
        self.assertIn("BMI = 25.469", bmi(weight, height))        
        self.assertIn("اضافه وزن", bmi(weight, height))
    def test4(self):
        weight = 78
        height = 1.60
        self.assertIn("BMI = 30.469", bmi(weight, height))        
        self.assertIn("چاقی درجه یک", bmi(weight, height))
    def test5(self):
        weight = 85
        height = 1.52
        self.assertIn("BMI = 36.790", bmi(weight, height))        
        self.assertIn("چاقی درجه دو", bmi(weight, height))
    def test6(self):
        weight = 95
        height = 1.50
        self.assertIn("BMI = 42.222", bmi(weight, height))        
        self.assertIn("چاقی درجه سه", bmi(weight, height))        

class test_prices_tool(unittest.TestCase):
    def test1(self):
        currency_name = "دلار"
        self.assertIn("قیمت دلار", prices(currency_name))
    def test2(self):
        currency_name = "کوله پشتی"
        self.assertIn("اطلاعاتی درمورد این ارز ندارم", prices(currency_name))

class test_date_difference_tool(unittest.TestCase):
    @patch("Backpack.date")
    def test_CE_date(self, mock_date):
        mock_date.today.return_value = real_date(2026, 8, 16)
        year = 2007
        month = 5
        day = 22
        self.assertEqual(date_difference_CE(year, month, day), "اختلاف تاریخ: 19 سال و 2 ماه و 25 روز")
    @patch("Backpack.jdatetime.date")
    def test_CE_date(self, mock_date):
        mock_date.today.return_value = real_persian_date(1405, 5, 25)
        year = 1404
        month = 2
        day = 12
        self.assertEqual(shamsi_date_difference(year, month, day), "اختلاف تاریخ: 1 سال و 3 ماه و 13 روز")

class test_translator_tool(unittest.TestCase):
    def test1(self):
        user_text = "Hello world"
        user_target_language = "فارسی"
        self.assertEqual(translator(user_text, user_target_language), "سلام دنیا")
    def test2(self):
        user_text = "سلام"
        user_target_language = "چینی"
        self.assertEqual(translator(user_text, user_target_language), "你好")

class test_lottery_tool(unittest.TestCase):
    def test1(self):
        user_text = "ماهان زهرا فاطمه مهدی"
        self.assertIn(lottery(user_text), user_text)            


if __name__ == "__main__":
    unittest.main()