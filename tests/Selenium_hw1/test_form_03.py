import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_text_box_submit():
    # 1. Запуск браузера Chrome
    driver = webdriver.Chrome()

    try:
        # 2. Открытие страницы
        driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
        driver.maximize_window()
        time.sleep(5)  # Пауза, чтобы визуально заметить открытие

        # 3. Поиск элементов и заполнение полей
        full_name_field = driver.find_element(By.ID, "userName")
        full_name_field.send_keys("John Doe")

        email_field = driver.find_element(By.ID, "userEmail")
        email_field.send_keys("john@example.com")

        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()
        print("Submit button")

        # 4. Проверка результата
        time.sleep(5)  # Пауза, чтобы увидеть результат отправки

        result_box = driver.find_element(By.ID, "output")
        result_text = result_box.get_attribute("textContent")
        print(result_text)

        # Проверяем, что в блоке результата появился введенный текст
        assert "John Doe" in result_text
        print("Тест успешно пройден!")

    finally:
        # 5. Закрытие браузера в любом случае
        driver.quit()