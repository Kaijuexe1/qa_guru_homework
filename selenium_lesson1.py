import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://qa-guru.github.io/one-page-form/text-box.html"


def open_page(driver):
    driver.get(URL)
    driver.maximize_window()


def fill_form(driver, name, email, current, permanent):
    driver.find_element(By.ID, "userName").send_keys(name)
    driver.find_element(By.ID, "userEmail").send_keys(email)
    driver.find_element(By.ID, "currentAddress").send_keys(current)
    driver.find_element(By.ID, "permanentAddress").send_keys(permanent)
    driver.find_element(By.ID, "submit").click()


def get_output(driver):
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "output"))
    )
    return driver.find_element(By.ID, "output").text


# =========================
# ПОЗИТИВНЫЙ ТЕСТ
# =========================

driver = webdriver.Chrome()

try:
    open_page(driver)

    fill_form(
        driver,
        "Иван Иванов",
        "ivan@example.com",
        "Москва",
        "Санкт-Петербург"
    )

    result = get_output(driver)

    assert "Иван Иванов" in result
    assert "ivan@example.com" in result
    assert "Москва" in result
    assert "Санкт-Петербург" in result

    print("Позитивный тест пройден!")

finally:
    driver.quit()


# =========================
# ПУСТОЙ CURRENT ADDRESS
# =========================

driver = webdriver.Chrome()

try:
    open_page(driver)

    fill_form(
        driver,
        "User Test",
        "test@test.com",
        "",
        "Казань"
    )

    result = get_output(driver)

    assert "Казань" in result

    print("Пустой current address пройден!")

finally:
    driver.quit()


# =========================
# ДЛИННЫЙ CURRENT ADDRESS
# =========================

driver = webdriver.Chrome()

try:
    open_page(driver)

    long_address = "Москва " * 50

    fill_form(
        driver,
        "Long User",
        "long@test.com",
        long_address,
        "Самара"
    )

    result = get_output(driver)

    assert long_address in result

    print("Длинный address тест пройден!")

finally:
    driver.quit()


# =========================
# СПЕЦСИМВОЛЫ В ADDRESS
# =========================

driver = webdriver.Chrome()

try:
    open_page(driver)

    special = "!@#$%^&*()_+"

    fill_form(
        driver,
        "Special User",
        "special@test.com",
        special,
        special
    )

    result = get_output(driver)

    assert special in result

    print("Спецсимволы в address пройдены!")

finally:
    driver.quit()


# =========================
# ОДИНАКОВЫЕ АДРЕСА
# =========================

driver = webdriver.Chrome()

try:
    open_page(driver)

    address = "Новосибирск"

    fill_form(
        driver,
        "Same User",
        "same@test.com",
        address,
        address
    )

    result = get_output(driver)

    assert result.count(address) == 2

    print("Одинаковые address пройдены!")

finally:
    driver.quit()


# =========================
# НЕГАТИВНЫЙ EMAIL (БЕЗ @)
# =========================

driver = webdriver.Chrome()

try:
    open_page(driver)

    fill_form(
        driver,
        "Bad Email",
        "petryandex.ru",
        "Москва",
        "СПб"
    )

    outputs = driver.find_elements(By.ID, "output")

    assert len(outputs) == 0

    print("Негативный email пройден!")

finally:
    driver.quit()


# =========================
# ПУСТОЙ EMAIL
# =========================

driver = webdriver.Chrome()

try:
    open_page(driver)

    fill_form(
        driver,
        "Empty Email",
        "",
        "Москва",
        "СПб"
    )

    outputs = driver.find_elements(By.ID, "output")

    assert len(outputs) == 0

    print("Пустой email пройден!")

finally:
    driver.quit()


# =========================
# SQL INJECTION
# =========================

driver = webdriver.Chrome()

try:
    open_page(driver)

    fill_form(
        driver,
        "SQL Hacker",
        "' OR 1=1 --",
        "Москва",
        "СПб"
    )

    outputs = driver.find_elements(By.ID, "output")

    assert len(outputs) == 0

    print("SQL injection тест пройден!")

finally:
    driver.quit()


# =========================
# СПЕЦСИМВОЛЫ EMAIL
# =========================

driver = webdriver.Chrome()

try:
    open_page(driver)

    fill_form(
        driver,
        "User",
        "!@#$%^&*",
        "Москва",
        "СПб"
    )

    outputs = driver.find_elements(By.ID, "output")

    assert len(outputs) == 0

    print("Спецсимволы email тест пройден!")

finally:
    driver.quit()


# =========================
# СЛИШКОМ ДЛИННЫЙ EMAIL
# =========================

driver = webdriver.Chrome()

try:
    open_page(driver)

    long_email = "a" * 300 + "@gmail.com"

    fill_form(
        driver,
        "Long Email",
        long_email,
        "Москва",
        "СПб"
    )

    outputs = driver.find_elements(By.ID, "output")

    assert len(outputs) == 0

    print("Длинный email тест пройден!")

finally:
    driver.quit()