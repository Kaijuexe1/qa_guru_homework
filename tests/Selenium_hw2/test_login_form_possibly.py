# 100% черновик, требует модификаци

# Задача: "Разработать на языке Python и библиотеке Selenium как можно больше позитивных и негативных тестовых сценариев используя подход DDT для формы логина https://qa-guru.github.io/one-page-form/login.html"
# Для реализации тестирования формы авторизации по методу DDT (Data-Driven Testing) на Python лучше всего использовать связку фреймворка pytest
# (через встроенную параметризацию @pytest.mark.parametrize) и библиотеки Selenium WebDriver.
# Ниже представлена подборка тестовых сценариев и готовый скрипт, автоматизирующий проверку страницы https://qa-guru.github.io/one-page-form/login.html .
# Спроектированные тестовые сценарии (DDT-матрица)В качестве валидных учетных данных (ожидаемое поведение тестового стенда QA.GURU) принята стандартная пара: email qaguru@qa.guru и любой непустой пароль (или специфичный qaguru),
# при которых форма показывает успешный вход.
# Позитивные сценарии (Positive)Валидный Email и пароль: Проверка классического успешного входа (qaguru@qa.guru).
# Регистронезависимость Email: Ввод email в верхнем регистре (QAGURU@QA.GURU) — система должна корректно приводить его к нижнему регистру.
# Негативные сценарии (Negative)Неверный пароль: Валидный email, но абсолютно некорректный пароль.
# Несуществующий Email: Попытка входа с незарегистрированной почтой.
# Пустой Email: Поле пароля заполнено, email — пустая строка (валидация обязательного поля).
# Пустой пароль: Поле email заполнено, пароль — пустая строка.
# Оба поля пустые: Отправка полностью пустой формы.
# Email без коммерческого атта @: Нарушение базового синтаксиса почты (qaguruqa.guru).Email без доменной части: Строка вида qaguru@.Email без имени ящика: Строка вида @qa.guru.
# Спецсимволы в Email: Использование запрещенных символов (qaguru!#$@qa.guru).Длинный пароль/Email (XSS/SQL-инъекции): Базовый чек на устойчивость к инъекциям (' OR '1'='1).

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://qa-guru.github.io/one-page-form/login.html?ru"  # ?ru -> сообщения на русском

# Реальные локаторы, снятые с фактического HTML страницы
LOGIN_INPUT = (By.ID, "login-input")
PASSWORD_INPUT = (By.ID, "password-input")
SUBMIT_BUTTON = (By.ID, "submit-button")
ERROR_MESSAGE = (By.ID, "error-message")
WELCOME_MESSAGE = (By.ID, "welcome-message")

# Валидные креды по умолчанию (страница сама кладёт их в localStorage при первом заходе)
VALID_LOGIN = "user1"
VALID_PASSWORD = "password1"


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()


@pytest.mark.parametrize(
    "login, password, scenario_type, expected_text",
    [
        # --- ПОЗИТИВНЫЕ ---
        (VALID_LOGIN, VALID_PASSWORD, "positive", f"Добро пожаловать, {VALID_LOGIN}!"),

        # --- НЕГАТИВНЫЕ ---
        (VALID_LOGIN, "wrongpass1", "negative", "Неверный логин или пароль"),
        ("unknownuser", VALID_PASSWORD, "negative", "Неверный логин или пароль"),
        ("", VALID_PASSWORD, "negative", "Укажите логин"),
        (VALID_LOGIN, "", "negative", "Укажите пароль"),
        ("", "", "negative", "Укажите логин и пароль"),
        ("ab", VALID_PASSWORD, "negative", "Логин должен содержать не менее 3 символов"),
        (VALID_LOGIN, "123", "negative", "Пароль должен содержать не менее 6 символов"),
        ("' OR '1'='1", "' OR '1'='1", "negative", "Неверный логин или пароль"),  # проверка на SQL-инъекцию
    ],
)
def test_login_form(driver, login, password, scenario_type, expected_text):
    driver.get(URL)

    login_field = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(LOGIN_INPUT))
    password_field = driver.find_element(*PASSWORD_INPUT)

    login_field.clear()
    login_field.send_keys(login)

    password_field.clear()
    password_field.send_keys(password)

    driver.find_element(*SUBMIT_BUTTON).click()

    if scenario_type == "positive":
        result = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(WELCOME_MESSAGE)
        )
        assert expected_text in result.text, (
            f"Ожидался успешный вход, получено: '{result.text}'"
        )
    else:
        result = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(ERROR_MESSAGE)
        )
        assert expected_text in result.text, (
            f"Форма повела себя иначе, чем ожидалось: "
            f"login='{login}', password='{password}', получено: '{result.text}'"
        )