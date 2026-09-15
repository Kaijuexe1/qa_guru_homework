import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    drv = webdriver.Chrome()
    yield drv
    drv.quit()


@pytest.fixture
def url():
    return "https://qa-guru.github.io/one-page-form/text-box.html"


class TestSuite:
    def test_case01(self, driver, url):
        # 2. Открытие страницы
        driver.get(url)
        driver.maximize_window()
        time.sleep(5)  # Пауза, чтобы визуально заметить открытие

        # 3. Поиск элементов и заполнение полей
        full_name_field = driver.find_element(By.ID, "userName")
        full_name_field.send_keys("John Doe")

        email_field = driver.find_element(By.ID, "userEmail")
        email_field.send_keys("john@example.com")

        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()

        # 4. Проверка результата
        time.sleep(5)  # Пауза, чтобы увидеть результат отправки

        result_box = driver.find_element(By.ID, "output")
        assert "John Doe" in result_box.text
        print("Тест 01 успешно пройден!")

    def test_case02(self, driver, url):
        # 2. Открытие страницы
        driver.get(url)
        driver.maximize_window()
        time.sleep(5)  # Пауза, чтобы визуально заметить открытие

        # 3. Поиск элементов и заполнение полей
        full_name_field = driver.find_element(By.ID, "userName")
        full_name_field.send_keys("John Doe")

        email_field = driver.find_element(By.ID, "userEmail")
        email_field.send_keys("john@example.com")

        permanent_address_field = driver.find_element(By.ID, "permanentAddress")
        permanent_address_field.send_keys("United States, New York, 5th avenue")

        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()

        # 4. Проверка результата
        time.sleep(5)  # Пауза, чтобы увидеть результат отправки

        result_box = driver.find_element(By.ID, "output")
        assert "John Doe" in result_box.text
        print("Тест 02 успешно пройден!")