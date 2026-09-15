import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Локаторы элементов формы на странице
LOGIN_INPUT = (By.ID, "login-input")
PASSWORD_INPUT = (By.ID, "password-input")
SUBMIT_BUTTON = (By.ID, "submit-button")
ERROR_MESSAGE = (By.ID, "error-message")
WELCOME_MESSAGE = (By.ID, "welcome-message")

VALID_LOGIN = "user1"
VALID_PASSWORD = "password1"


@pytest.fixture
def driver():
    """Фикстура для инициализации и закрытия браузера."""
    driver = webdriver.Chrome()
    driver.maximize_window()

    yield driver

    driver.quit()


# Реализация DDT подхода через параметризацию pytest.
# Данные приведены к реальной логике формы: это поле "Логин" (не Email!),
# без валидации на @ — только минимальная длина (login >= 3, password >= 6),
# и стандартные креды по умолчанию user1/password1. Страница без ?ru
# в URL => сообщения на английском.
@pytest.mark.parametrize(
    "login, password, scenario_type, expected_text",
    [
        # --- ПОЗИТИВНЫЕ СЦЕНАРИИ ---
        (VALID_LOGIN, VALID_PASSWORD, "positive", f"Welcome, {VALID_LOGIN}!"),

        # --- НЕГАТИВНЫЕ СЦЕНАРИИ ---
        (VALID_LOGIN, "wrong_pass1", "negative", "Wrong login or password"),
        ("unknown_user", VALID_PASSWORD, "negative", "Wrong login or password"),
        ("", VALID_PASSWORD, "negative", "Login is required"),
        (VALID_LOGIN, "", "negative", "Password is required"),
        ("", "", "negative", "Login and password are required"),
        ("ab", VALID_PASSWORD, "negative", "Login must be at least 3 characters"),
        (VALID_LOGIN, "123", "negative", "Password must be at least 6 characters"),
        ("' OR '1'='1", "' OR '1'='1", "negative", "Wrong login or password"),
    ],
)
def test_login_form(driver, login, password, scenario_type, expected_text):
    """Тест кейс, принимающий наборы данных (DDT)."""

    # 1. Открытие тестируемой страницы
    driver.get("https://qa-guru.github.io/one-page-form/login.html")

    # 2. Поиск элементов формы
    login_field = driver.find_element(*LOGIN_INPUT)
    password_field = driver.find_element(*PASSWORD_INPUT)
    submit_button = driver.find_element(*SUBMIT_BUTTON)

    # 3. Очистка полей и ввод тестовых данных
    login_field.clear()
    login_field.send_keys(login)

    password_field.clear()
    password_field.send_keys(password)

    # 4. Клик по кнопке отправки формы
    submit_button.click()

    # 5. Ожидание ответа — ОДИН explicit wait на нужный элемент.
    #
    # В исходном файле здесь было СРАЗУ ТРИ анти-паттерна:
    #   1) implicit_wait(5) вперемешку с явным WebDriverWait(driver, 2)
    #      для алерта — Selenium официально не рекомендует смешивать
    #      implicit и explicit wait: таймауты складываются непредсказуемо,
    #      тесты то тормозят сильнее ожидаемого, то падают раньше времени.
    #   2) голый `except:` — ловит вообще всё (включая программные
    #      ошибки типа опечатки в локаторе), и на этом сайте эта ветка
    #      всегда срабатывала бы, потому что тут нет ни одного нативного
    #      browser alert — только JS, рисующий текст в <p id="error-message">.
    #      То есть весь try/except был мёртвым кодом.
    #   3) result уже читался один раз ДО time.sleep(5), а потом ещё раз
    #      читался ПОСЛЕ — то есть значение вычислялось дважды, а между
    #      этим стоял жёсткий sleep на 5 секунд, который просто тормозил
    #      каждый из 9 тестов на ровном месте, сводя на нет весь смысл
    #      explicit wait.
    if scenario_type == "positive":
        result = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(WELCOME_MESSAGE)
        )
    else:
        result = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(ERROR_MESSAGE)
        )

    actual_result = result.text

    # 6. Проверка результата (Assertion)
    assert expected_text in actual_result, (
        f"login='{login}', password='{password}': "
        f"ожидалось '{expected_text}', получено '{actual_result}'"
    )
