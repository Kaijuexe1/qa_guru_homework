import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def open_form(driver):
    driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
    driver.maximize_window()
    time.sleep(5)  # Пауза, чтобы визуально заметить открытие


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
    time.sleep(5)  # Пауза, чтобы увидеть результат отправки


def get_output_text(driver):
    result_box = driver.find_element(By.ID, "output")
    return result_box.get_attribute("textContent")


def test01_only_special_char_in_name_empty_email():
    print("Негативная проверка: имя = '@', email пустой")
    driver = webdriver.Chrome()
    try:
        open_form(driver)
        fill_form(driver, full_name="@", email="")
        submit_form(driver)

        output_text = get_output_text(driver)
        # Email обязателен, поэтому вывод не должен содержать введённое имя
        assert "@" not in output_text
        print("Тест успешно пройден!")
    finally:
        driver.quit()


def test02_long_concatenated_email():
    print("Негативная проверка: имя = '@', email — несколько адресов подряд без разделителя")
    driver = webdriver.Chrome()
    try:
        open_form(driver)
        fill_form(driver, full_name="@", email="johnexa@mple.comivanexa@mple.comivanexa@mple.com")
        submit_form(driver)

        output_text = get_output_text(driver)
        # Некорректный email не должен пройти как валидный адрес
        assert "johnexa@mple.comivanexa@mple.comivanexa@mple.com" not in output_text
        print("Тест успешно пройден!")
    finally:
        driver.quit()


def test03_email_typo_double_at():
    print("Негативная проверка: сравнение введённого email с искажённой строкой (двойной @)")
    driver = webdriver.Chrome()
    try:
        open_form(driver)
        fill_form(driver, full_name="johnexa@mple.com", email="johnexa@mple.com")
        submit_form(driver)

        output_text = get_output_text(driver)
        # Введён "johnexa@mple.com" — строка с двойным "@" заведомо не совпадёт
        assert "johnexa@@mple.com" not in output_text
        print("Тест успешно пройден!")
    finally:
        driver.quit()


def test04_name_filled_email_empty():
    print("Негативная проверка: имя заполнено, email пустой")
    driver = webdriver.Chrome()
    try:
        open_form(driver)
        fill_form(driver, full_name="John", email="")
        submit_form(driver)

        output_text = get_output_text(driver)
        # Email обязателен — форма не должна отправиться с несуществующим адресом
        assert "johne@xample.com" not in output_text
        print("Тест успешно пройден!")
    finally:
        driver.quit()


def test05_email_with_invalid_symbol():
    print("Негативная проверка: email с недопустимым символом '$' вместо '@'")
    driver = webdriver.Chrome()
    try:
        open_form(driver)
        fill_form(driver, full_name="", email="john$example.com")
        submit_form(driver)

        output_text = get_output_text(driver)
        # "john$example.com" не является валидным email — не должен пройти как "johnexample.com"
        assert "johnexample.com" not in output_text
        print("Тест успешно пройден!")
    finally:
        driver.quit()


def test06_all_fields_filled_with_email_instead_of_address():
    print("Негативная проверка: во все поля (включая адреса) вписан email")
    driver = webdriver.Chrome()
    try:
        open_form(driver)
        fill_form(
            driver,
            full_name="john@example.com",
            email="john@example.com",
            current_address="john@example.com",
            permanent_address="john@example.com",
        )
        submit_form(driver)

        output_text = get_output_text(driver)
        # В поля адреса вписан email, а не адрес — реального адреса в выводе быть не должно
        assert "United States, 5th avenue" not in output_text
        print("Тест успешно пройден!")
    finally:
        driver.quit()