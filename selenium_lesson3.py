import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"

browser = webdriver.Chrome()
browser.get(URL)

class PracticeForm:

    #INPUTS
    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    EMAIL = (By.ID, "email")
    MOBILE = (By.ID, "mobile")
    CURRENT_ADDRESS = (By.ID, "currentAddress")

    #GENDER
    GENDER = (By.ID, "gender")
    GENDER_MALE = (By.ID, "gender_male")
    GENDER_FEMALE = (By.ID, "gender_female")
    GENDER_OTHER = (By.ID, "gender_other")

    #HOBBIES
    HOBBIES = (By.ID, "hobbies")
    HOBBIES_SPORTS = (By.ID, "hobbies_sports")
    HOBBIES_READING = (By.ID, "hobbies_reading")
    HOBBIES_MUSIC = (By.ID, "hobbies_music")