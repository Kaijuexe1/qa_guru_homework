from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class PracticeFormPage:

    # =====================================
    # URL
    # =====================================

    URL = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"

    # =====================================
    # ЛОКАТОРЫ
    # =====================================

    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    EMAIL = (By.ID, "userEmail")

    MALE = (By.XPATH, "//label[@for='gender-radio-1']")
    FEMALE = (By.XPATH, "//label[@for='gender-radio-2']")

    MOBILE = (By.ID, "userNumber")

    DATE_INPUT = (By.ID, "dateOfBirthInput")

    SUBJECTS = (By.ID, "subjectsInput")

    SPORTS = (By.XPATH, "//label[@for='hobbies-checkbox-1']")
    READING = (By.XPATH, "//label[@for='hobbies-checkbox-2']")
    MUSIC = (By.XPATH, "//label[@for='hobbies-checkbox-3']")

    UPLOAD_PICTURE = (By.ID, "uploadPicture")

    ADDRESS = (By.ID, "currentAddress")

    STATE = (By.ID, "state")
    CITY = (By.ID, "city")

    SUBMIT = (By.ID, "submit")

    RESULT_TABLE = (By.CLASS_NAME, "table-responsive")

    # =====================================
    # INIT
    # =====================================

    def __init__(self, driver):
        self.driver = driver

    # =====================================
    # МЕТОДЫ
    # =====================================

    def open(self):
        self.driver.get(self.URL)

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.FIRST_NAME)
        )

        self.driver.execute_script(
            "document.querySelector('footer')?.remove();"
        )

        self.driver.execute_script(
            "document.getElementById('fixedban')?.remove();"
        )

        self.driver.maximize_window()

    def fill_basic_form(
        self,
        first_name,
        last_name,
        email,
        phone,
        address
    ):
        self.driver.find_element(*self.FIRST_NAME).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME).send_keys(last_name)
        self.driver.find_element(*self.EMAIL).send_keys(email)

        self.driver.find_element(*self.MALE).click()

        self.driver.find_element(*self.MOBILE).send_keys(phone)

        self.driver.find_element(*self.ADDRESS).send_keys(address)

    def set_birth_date(self):
        self.driver.execute_script(
            "document.getElementById('dateOfBirthInput').value = '01/01/2000';"
        )
        self.driver.find_element(By.TAG_NAME, "body").click()

    def set_subject(self, subject):
        field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.SUBJECTS)
        )
        field.send_keys(subject)
        field.send_keys(Keys.ENTER)

    def select_hobby_sports(self):
        self.driver.find_element(*self.SPORTS).click()

    def upload_file(self, filepath):
        self.driver.find_element(
            *self.UPLOAD_PICTURE
        ).send_keys(filepath)

    def select_state_city(self):

        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            self.driver.find_element(*self.STATE)
        )

        self.driver.find_element(*self.STATE).click()

        self.driver.find_element(
            By.XPATH,
            "//div[text()='NCR']"
        ).click()

        self.driver.find_element(*self.CITY).click()

        self.driver.find_element(
            By.XPATH,
            "//div[text()='Delhi']"
        ).click()

    def submit(self):

        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            self.driver.find_element(*self.SUBMIT)
        )

        self.driver.find_element(*self.SUBMIT).click()

    def get_result(self):

        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(
                self.RESULT_TABLE
            )
        )

        return self.driver.find_element(
            *self.RESULT_TABLE
        ).text

    def get_email_validation_message(self):

        return self.driver.find_element(
            *self.EMAIL
        ).get_attribute("validationMessage")


# =====================================
# SETUP / TEARDOWN
# =====================================

def set_up():

    driver = webdriver.Chrome()

    driver.implicitly_wait(5)

    page = PracticeFormPage(driver)

    page.open()

    return driver, page


def tear_down(driver):
    driver.quit()


# =====================================
# ПОЗИТИВНЫЙ ТЕСТ
# =====================================

def test_positive():

    driver, page = set_up()

    try:

        page.fill_basic_form(
            "Иван",
            "Иванов",
            "ivan@test.com",
            "9999999999",
            "Москва"
        )

        page.set_birth_date()

        page.set_subject("Maths")

        page.select_hobby_sports()

        page.select_state_city()

        page.submit()

        result = page.get_result()

        assert "Иван Иванов" in result
        assert "ivan@test.com" in result
        assert "9999999999" in result
        assert "Maths" in result
        assert "Sports" in result
        assert "Delhi" in result

        print("✓ Позитивный тест")

    finally:
        tear_down(driver)


# =====================================
# EMAIL БЕЗ @
# =====================================

def test_invalid_email():

    driver, page = set_up()

    try:

        page.fill_basic_form(
            "User",
            "Test",
            "testmail.ru",
            "9999999999",
            "Москва"
        )

        assert (
            page.get_email_validation_message()
            != ""
        )

        print("✓ Email без @ отклонен")

    finally:
        tear_down(driver)


# =====================================
# ПУСТОЙ АДРЕС
# =====================================

def test_empty_address():

    driver, page = set_up()

    try:

        page.fill_basic_form(
            "User",
            "Test",
            "test@test.com",
            "9999999999",
            ""
        )

        page.submit()

        result = page.get_result()

        assert "User Test" in result

        print("✓ Пустой адрес")

    finally:
        tear_down(driver)


# =====================================
# ДЛИННЫЙ АДРЕС
# =====================================

def test_long_address():

    driver, page = set_up()

    try:

        address = "Москва " * 100

        page.fill_basic_form(
            "Long",
            "User",
            "long@test.com",
            "9999999999",
            address
        )

        page.submit()

        result = page.get_result()

        assert "Москва" in result

        print("✓ Длинный адрес")

    finally:
        tear_down(driver)


# =====================================
# SQL INJECTION EMAIL
# =====================================

def test_sql_email():

    driver, page = set_up()

    try:

        page.fill_basic_form(
            "SQL",
            "User",
            "' OR 1=1 --",
            "9999999999",
            "Москва"
        )

        assert (
            page.get_email_validation_message()
            != ""
        )

        print("✓ SQL email отклонён")

    finally:
        tear_down(driver)


# =====================================
# КОРОТКИЙ ТЕЛЕФОН
# =====================================

def test_short_phone():

    driver, page = set_up()

    try:

        page.fill_basic_form(
            "Phone",
            "User",
            "user@test.com",
            "12345",
            "Москва"
        )

        page.submit()

        modal = driver.find_elements(
            By.CLASS_NAME,
            "modal-content"
        )

        assert len(modal) == 0

        print("✓ Телефон менее 10 цифр")

    finally:
        tear_down(driver)


# =====================================
# ДЛИННЫЙ ТЕЛЕФОН
# =====================================

def test_long_phone():

    driver, page = set_up()

    try:

        page.fill_basic_form(
            "Phone",
            "User",
            "user@test.com",
            "123456789012345",
            "Москва"
        )

        value = driver.find_element(
            *page.MOBILE
        ).get_attribute("value")

        assert len(value) <= 10

        print("✓ Ограничение телефона")

    finally:
        tear_down(driver)


# =====================================
# SUBJECTS
# =====================================

def test_subjects():

    driver, page = set_up()

    try:

        page.fill_basic_form(
            "Math",
            "User",
            "math@test.com",
            "9999999999",
            "Москва"
        )

        page.set_subject("Physics")

        page.submit()

        result = page.get_result()

        assert "Physics" in result

        print("✓ Subjects")

    finally:
        tear_down(driver)


# =====================================
# HOBBIES
# =====================================

def test_hobbies():

    driver, page = set_up()

    try:

        page.fill_basic_form(
            "Sport",
            "User",
            "sport@test.com",
            "9999999999",
            "Москва"
        )

        page.select_hobby_sports()

        page.submit()

        result = page.get_result()

        assert "Sports" in result

        print("✓ Hobbies")

    finally:
        tear_down(driver)


# =====================================
# FILE UPLOAD
# =====================================

def test_file_upload():

    driver, page = set_up()

    try:

        test_file = os.path.abspath(__file__)

        page.fill_basic_form(
            "File",
            "User",
            "file@test.com",
            "9999999999",
            "Москва"
        )

        page.upload_file(test_file)

        page.submit()

        result = page.get_result()

        assert os.path.basename(
            test_file
        ) in result

        print("✓ Upload file")

    finally:
        tear_down(driver)


# =====================================
# STATE + CITY
# =====================================

def test_state_city():

    driver, page = set_up()

    try:

        page.fill_basic_form(
            "State",
            "User",
            "state@test.com",
            "9999999999",
            "Москва"
        )

        page.select_state_city()

        page.submit()

        result = page.get_result()

        assert "NCR Delhi" in result

        print("✓ State / City")

    finally:
        tear_down(driver)


# =====================================
# ЗАПУСК
# =====================================

if __name__ == "__main__":

    test_positive()
    test_invalid_email()
    test_empty_address()
    test_long_address()
    test_sql_email()
    test_short_phone()
    test_long_phone()
    test_subjects()
    test_hobbies()
    test_file_upload()
    test_state_city()

    print("\nВсе тесты успешно завершены.")
