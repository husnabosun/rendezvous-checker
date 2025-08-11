import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc


# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)
    
    
EMAIL = config["EMAIL"]
PASSWORD = config["PASSWORD"]
URL = config["URL"]
    
chrome_options = Options()

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

        todays_date = "11 Ağustos"
        pick_date_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[@title='{todays_date}']"))
        )
        pick_date_btn.click()
        print("Appointment date is chosen for today")

        submit_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID,"ContentPlaceHolder1_BtnRandevuAl"))
        )
        submit_btn.click()
        print("The appointment is submitted")

    except Exception as e:
        print(f"An error occured during login: {e}")
        driver.quit()
        exit()


# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Extract configuration values
sleep_min_seconds = config["sleep_min_seconds"]
sleep_max_seconds = config["sleep_max_seconds"]
chrome_driver_path = config["chrome_driver_path"]


login_sks(driver)

try:
    driver.quit()
except Exception:
    pass