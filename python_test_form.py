import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Локаторы
FULL_NAME = (By.ID, "userName")
EMAIL = (By.ID, "userEmail")
SUBMIT_BUTTON = (By.ID, "submit")
RESULT_BOX = (By.ID, "output")


def test_01():
    print("Первая итерация")

    # Запуск браузера
    driver = webdriver.Chrome()

    try:
        # Открытие страницы
        driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
        driver.maximize_window()

        #Пауза для просмотра
        time.sleep(2)

        wait = WebDriverWait(driver, 10)

        # Заполнение формы
        wait.until(
            EC.visibility_of_element_located(FULL_NAME)
        ).send_keys("Иван Иванов")

        # Пауза для просмотра
        time.sleep(1)

        driver.find_element(*EMAIL).send_keys("ivan@example.com")

        # Пауза для просмотра
        time.sleep(1)

        # Отправка формы
        driver.find_element(*SUBMIT_BUTTON).click()

        # Пауза для просмотра
        time.sleep(2)

        # Проверка результата
        result_box = wait.until(
            EC.visibility_of_element_located(RESULT_BOX)
        )

        assert "Иван Иванов" in result_box.text

        print("Тест успешно пройден!")

        # Пауза для просмотра
        time.sleep(2)

    finally:
        driver.quit()
