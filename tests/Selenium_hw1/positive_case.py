import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_for_all_fields():
    print("Рефакторинг - итерация 1!")

    driver = webdriver.Chrome()

    try:
        driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
        driver.maximize_window()
        time.sleep(5)  # Пауза, чтобы визуально заметить открытие

        full_name_field = driver.find_element(By.ID, "userName")
        full_name_field.send_keys("John Doe")

        email_field = driver.find_element(By.ID, "userEmail")
        email_field.send_keys("johndoe@example.com")

        current_address_field = driver.find_element(By.ID, "currentAddress")
        current_address_field.send_keys("United States, 5th avenue")

        permanent_address_field = driver.find_element(By.ID, "permanentAddress")
        permanent_address_field.send_keys("United States, 5th avenue")

        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()

        time.sleep(5)  # Пауза, чтобы увидеть результат отправки

        result_box = driver.find_element(By.ID, "output")
        output_text = result_box.get_attribute("textContent")

        assert "United States, 5th avenue" in output_text
        print("Тест успешно пройден!")

    finally:
        driver.quit()