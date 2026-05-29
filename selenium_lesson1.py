import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# =========================
# ПОЗИТИВНЫЙ ТЕСТ
# =========================

driver = webdriver.Chrome()

try:
    driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
    driver.maximize_window()

    # Full Name
    full_name_field = driver.find_element(By.ID, "userName")
    full_name_field.send_keys("Иван Иванов")

    # Email
    email_field = driver.find_element(By.ID, "userEmail")
    email_field.send_keys("ivan@example.com")

    # Current Address
    current_address = driver.find_element(By.ID, "currentAddress")
    current_address.send_keys("Москва")

    # Permanent Address
    permanent_address = driver.find_element(By.ID, "permanentAddress")
    permanent_address.send_keys("Санкт-Петербург")

    # Submit
    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()

    time.sleep(2)

    # Проверка результата
    result_box = driver.find_element(By.ID, "output")

    assert "Иван Иванов" in result_box.text
    assert "ivan@example.com" in result_box.text
    assert "Москва" in result_box.text
    assert "Санкт-Петербург" in result_box.text

    print("Позитивный тест успешно пройден!")

finally:
    driver.quit()


# =========================
# НЕГАТИВНЫЙ ТЕСТ
# EMAIL БЕЗ @
# =========================

driver = webdriver.Chrome()

try:
    driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
    driver.maximize_window()

    full_name_field = driver.find_element(By.ID, "userName")
    full_name_field.send_keys("Петр Петров")

    email_field = driver.find_element(By.ID, "userEmail")
    email_field.send_keys("petryandex.ru")

    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()

    time.sleep(2)

    result_box = driver.find_element(By.ID, "output")

    # Форма не должна отправиться
    assert result_box.text == ""

    print("Негативный тест без @ успешно пройден!")

finally:
    driver.quit()


# =========================
# НЕГАТИВНЫЙ ТЕСТ
# ПУСТОЙ EMAIL
# =========================

driver = webdriver.Chrome()

try:
    driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
    driver.maximize_window()

    full_name_field = driver.find_element(By.ID, "userName")
    full_name_field.send_keys("Сергей Сергеев")

    email_field = driver.find_element(By.ID, "userEmail")
    email_field.send_keys("")

    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()

    time.sleep(2)

    result_box = driver.find_element(By.ID, "output")

    assert result_box.text == ""

    print("Негативный тест пустого email успешно пройден!")

finally:
    driver.quit()


# =========================
# НЕГАТИВНЫЙ ТЕСТ
# SQL INJECTION
# =========================

driver = webdriver.Chrome()

try:
    driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
    driver.maximize_window()

    full_name_field = driver.find_element(By.ID, "userName")
    full_name_field.send_keys("SQL Hacker")

    email_field = driver.find_element(By.ID, "userEmail")
    email_field.send_keys("' OR 1=1 --")

    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()

    time.sleep(2)

    result_box = driver.find_element(By.ID, "output")

    assert result_box.text == ""

    print("Негативный SQL test успешно пройден!")

finally:
    driver.quit()

# =========================
# НЕГАТИВНЫЙ ТЕСТ
# СПЕЦСИМВОЛЫ
# =========================

driver = webdriver.Chrome()

try:
    driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
    driver.maximize_window()

    full_name_field = driver.find_element(By.ID, "userName")
    full_name_field.send_keys("Test User")

    email_field = driver.find_element(By.ID, "userEmail")
    email_field.send_keys("!@#$%^&*")

    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()

    time.sleep(2)

    result_box = driver.find_element(By.ID, "output")

    assert result_box.text == ""

    print("Негативный тест со спецсимволами успешно пройден!")

finally:
    driver.quit()


# =========================
# НЕГАТИВНЫЙ ТЕСТ
# СЛИШКОМ ДЛИННЫЙ EMAIL
# =========================

driver = webdriver.Chrome()

try:
    driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
    driver.maximize_window()

    full_name_field = driver.find_element(By.ID, "userName")
    full_name_field.send_keys("Long Email User")

    email_field = driver.find_element(By.ID, "userEmail")
    email_field.send_keys("a" * 300 + "@gmail.com")

    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()

    time.sleep(2)

    result_box = driver.find_element(By.ID, "output")

    assert result_box.text == ""

    print("Негативный тест длинного email успешно пройден!")

finally:
    driver.quit()
