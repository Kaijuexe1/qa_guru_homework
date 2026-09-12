import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def open_form(driver):
    driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
    driver.maximize_window()
    time.sleep(5)


def fill_form(driver, full_name=None, email=None, current_address=None, permanent_address=None):
    if full_name is not None:
        driver.find_element(By.ID, "userName").send_keys(full_name)
    if email is not None:
        driver.find_element(By.ID, "userEmail").send_keys(email)
    if current_address is not None:
        driver.find_element(By.ID, "currentAddress").send_keys(current_address)
    if permanent_address is not None:
        driver.find_element(By.ID, "permanentAddress").send_keys(permanent_address)


def submit_form(driver):
    driver.find_element(By.ID, "submit").click()
    time.sleep(5)


def get_output_text(driver):
    result_box = driver.find_element(By.ID, "output")
    return result_box.get_attribute("textContent")


def test07_current_and_permanent_address_validation():
    print("Негативная проверка: пустой current address + спецсимволы и длинная строка в permanent address")
    driver = webdriver.Chrome()
    try:
        open_form(driver)

        long_permanent_address = "<script>alert(1)</script> !@#$%^&*() " + "A" * 500

        fill_form(
            driver,
            full_name="John Doe",
            email="john@example.com",
            current_address="",
            permanent_address=long_permanent_address,
        )
        submit_form(driver)

        output_text = get_output_text(driver)
        current_address_value = driver.find_element(By.ID, "currentAddress").get_attribute("value")
        permanent_address_value = driver.find_element(By.ID, "permanentAddress").get_attribute("value")

        assert current_address_value == ""
        assert permanent_address_value == long_permanent_address
        assert "<script>" not in output_text
        assert "</script>" not in output_text
        assert "!@#$%^&*()" in output_text
        assert "A" * 500 in output_text

        print("Тест успешно пройден!")
    finally:
        driver.quit()