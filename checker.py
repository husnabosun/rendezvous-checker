import json
import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc


EMAIL = os.getenv["EMAIL"]
PASSWORD = os.getenv["PASSWORD"]
URL = os.getenv["URL"]
    
chrome_options = Options()
chrome_options.headless = True 
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ChromeDriver'ı otomatik indir ve kullan
service = Service(ChromeDriverManager().install())

driver = uc.Chrome()


def login_sks(driver):          
    try:
        print('Waiting for the login...')
        driver.get(URL)
        print('waiting for the form')
        email_field = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.NAME, "txtKullaniciAdi")))
        password_field = driver.find_element(By.NAME, 'txtParola')
        print('Filling the blanks')
        email_field.send_keys(EMAIL)
        password_field.send_keys(PASSWORD)

        print('Waiting for the login button')
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.NAME, "btnGiris"))
        )
        login_button.click()

        print('waiting for the login after items')
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CLASS_NAME, "logo-lg"))
        )
        print('Login has successfully completed.')

        menu_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[@href='#' and span[text()='Spor Tesis İşlemleri']]"))
        )

        menu_link.click()
        print("Menu link is successfully opened")

        appoint_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[@href='TesisRezervasyonListesi.aspx']"))
        )
        appoint_link.click()
        print("Appointment page is successfully opened")

        pool_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[@href='TesisRezervasyonListesi.aspx?NOKTA_KOD=14']"))
        )
        pool_btn.click()
        print("Pool option is chosen")

        see_dates_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[@href='RandevuAl.aspx?ID=97']"))
        )
        see_dates_btn.click()
        print("Heading to choosing date page")

        today_day = datetime.datetime.now().strftime("%d")
        today_month = datetime.datetime.now().strftime("%B")

        match today_month:
            case "January":
                today_month = "Ocak"
            case "February":
                today_month = "Şubat"
            case "March":
                today_month = "Mart"
            case "April":
                today_month = "Nisan"
            case "May":
                today_month = "Mayıs"
            case "June":
                today_month = "Haziran"
            case "July":
                today_month = "Temmuz"
            case "August":
                today_month = "Ağustos"
            case "September":
                today_month = "Eylül"
            case "October":
                today_month = "Ekim"
            case "November":
                today_month = "Kasım"
            case "December":
                today_month = "Aralık"
            
        todays_date = f"{today_day} {today_month}"
        
        
        pick_date_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[@title='{todays_date}']"))
        )
        pick_date_btn.click()
        print("Appointment date is chosen for today")
        
        
        time_list = ["15:30-16:45","14:00-15:15"]
        
        time_buttons = driver.find_elements(By.XPATH, "//label[contains(@class, 'btn') and contains(@class, 'rd-saat')]")
        time_btn_headers = []
        for i in time_buttons:
            span = i.find_element(By.TAG_NAME, "span").text
            time_btn_headers.append(span)
        
        print(time_btn_headers)
        
        for i in time_list:
            if i in time_btn_headers:
                pick_time_btn = driver.find_element(By.XPATH, f"//label[span[contains(text(),'{i}')]]/input[@type='radio']")
                pick_time_btn.click()
                print(f"Appointment is successfully choosed for {todays_date} , {i}")
                break

        submit_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID,"ContentPlaceHolder1_BtnRandevuAl"))
        )
        submit_btn.click()
        print("The appointment is submitted")

    except Exception as e:
        print(f"An error occured during login: {e}")
        driver.quit()
        exit()




login_sks(driver)

try:
    driver.quit()
except Exception:
    pass
