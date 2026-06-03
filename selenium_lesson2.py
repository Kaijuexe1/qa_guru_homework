from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TextBoxPage:
    URL = "https://qa-guru.github.io/one-page-form/text-box.html"

    USER_NAME = (By.ID, "userName")
    USER_EMAIL = (By.ID, "userEmail")
    CURRENT_ADDRESS = (By.ID, "currentAddress")
    PERMANENT_ADDRESS = (By.ID, "permanentAddress")
    SUBMIT_BUTTON = (By.ID, "submit")
    OUTPUT = (By.ID, "output")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)
        self.driver.maximize_window()

    def fill_form(self, name, email, current, permanent):
        self.driver.find_element(*self.USER_NAME).send_keys(name)
        self.driver.find_element(*self.USER_EMAIL).send_keys(email)
        self.driver.find_element(*self.CURRENT_ADDRESS).send_keys(current)
        self.driver.find_element(*self.PERMANENT_ADDRESS).send_keys(permanent)
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def get_output(self):
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.OUTPUT)
        )
        return self.driver.find_element(*self.OUTPUT).text

    def get_output_elements(self):
        return self.driver.find_elements(*self.OUTPUT)


def set_up():
    driver = webdriver.Chrome()
    page = TextBoxPage(driver)
    page.open()
    return driver, page


def tear_down(driver):
    driver.quit()


# =========================
# ПОЗИТИВНЫЙ ТЕСТ
# =========================

def test_positive():
    driver, page = set_up()

    try:
        page.fill_form(
            "Иван Иванов",
            "ivan@example.com",
            "Москва",
            "Санкт-Петербург"
        )

        result = page.get_output()

        assert "Иван Иванов" in result
        assert "ivan@example.com" in result
        assert "Москва" in result
        assert "Санкт-Петербург" in result

        print("Позитивный тест пройден!")

    finally:
        tear_down(driver)


# =========================
# ПУСТОЙ CURRENT ADDRESS
# =========================

def test_empty_current_address():
    driver, page = set_up()

    try:
        page.fill_form(
            "User Test",
            "test@test.com",
            "",
            "Казань"
        )

        result = page.get_output()

        assert "Казань" in result

        print("Пустой current address пройден!")

    finally:
        tear_down(driver)


# =========================
# ДЛИННЫЙ CURRENT ADDRESS
# =========================

def test_long_address():
    driver, page = set_up()

    try:
        long_address = "Москва " * 50

        page.fill_form(
            "Long User",
            "long@test.com",
            long_address,
            "Самара"
        )

        result = page.get_output()

        assert long_address in result

        print("Длинный address тест пройден!")

    finally:
        tear_down(driver)


# =========================
# СПЕЦСИМВОЛЫ В ADDRESS
# =========================

def test_special_symbols_address():
    driver, page = set_up()

    try:
        special = "!@#$%^&*()_+"

        page.fill_form(
            "Special User",
            "special@test.com",
            special,
            special
        )

        result = page.get_output()

        assert special in result

        print("Спецсимволы в address пройдены!")

    finally:
        tear_down(driver)


# =========================
# ОДИНАКОВЫЕ ADDRESS
# =========================

def test_same_addresses():
    driver, page = set_up()

    try:
        address = "Новосибирск"

        page.fill_form(
            "Same User",
            "same@test.com",
            address,
            address
        )

        result = page.get_output()

        assert result.count(address) == 2

        print("Одинаковые address пройдены!")

    finally:
        tear_down(driver)


# =========================
# НЕГАТИВНЫЙ EMAIL (БЕЗ @)
# =========================

def test_invalid_email_without_at():
    driver, page = set_up()

    try:
        page.fill_form(
            "Bad Email",
            "petryandex.ru",
            "Москва",
            "СПб"
        )

        outputs = page.get_output_elements()

        assert len(outputs) == 0

        print("Негативный email пройден!")

    finally:
        tear_down(driver)


# =========================
# ПУСТОЙ EMAIL
# =========================

def test_empty_email():
    driver, page = set_up()

    try:
        page.fill_form(
            "Empty Email",
            "",
            "Москва",
            "СПб"
        )

        outputs = page.get_output_elements()

        assert len(outputs) == 0

        print("Пустой email пройден!")

    finally:
        tear_down(driver)


# =========================
# SQL INJECTION
# =========================

def test_sql_injection_email():
    driver, page = set_up()

    try:
        page.fill_form(
            "SQL Hacker",
            "' OR 1=1 --",
            "Москва",
            "СПб"
        )

        outputs = page.get_output_elements()

        assert len(outputs) == 0

        print("SQL injection тест пройден!")

    finally:
        tear_down(driver)


# =========================
# СПЕЦСИМВОЛЫ EMAIL
# =========================

def test_special_symbols_email():
    driver, page = set_up()

    try:
        page.fill_form(
            "User",
            "!@#$%^&*",
            "Москва",
            "СПб"
        )

        outputs = page.get_output_elements()

        assert len(outputs) == 0

        print("Спецсимволы email тест пройден!")

    finally:
        tear_down(driver)


# =========================
# СЛИШКОМ ДЛИННЫЙ EMAIL
# =========================

def test_long_email():
    driver, page = set_up()

    try:
        long_email = "a" * 300 + "@gmail.com"

        page.fill_form(
            "Long Email",
            long_email,
            "Москва",
            "СПб"
        )

        outputs = page.get_output_elements()

        assert len(outputs) == 0

        print("Длинный email тест пройден!")

    finally:
        tear_down(driver)


# =========================
# ЗАПУСК ВСЕХ ТЕСТОВ
# =========================

test_positive()
test_empty_current_address()
test_long_address()
test_special_symbols_address()
test_same_addresses()
test_invalid_email_without_at()
test_empty_email()
test_sql_injection_email()
test_special_symbols_email()
test_long_email()

print("\nВсе тесты завершены.")