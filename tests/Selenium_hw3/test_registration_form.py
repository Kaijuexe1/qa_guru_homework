import os
import pytest
from registration_page import RegistrationPage


@pytest.fixture
def temp_picture():
    """Временный файл для поля upload — не хранит реальную картинку,
    Selenium просто подставляет путь в input[type=file]."""
    path = os.path.abspath("test_image.jpg")
    with open(path, "w") as f:
        f.write("fake image data")
    yield path
    if os.path.exists(path):
        os.remove(path)


def test_full_positive_submission(driver, temp_picture):
    page = RegistrationPage(driver).open()
    page.close_promo_banner_if_present()

    page.fill_full_form(
        first_name="Иван",
        last_name="Петров",
        email="ivan.petrov@example.com",
        phone="9991234567",
        address="123456, г. Москва, ул. Ленина, д. 1",
        subject="Computer Science",
        temp_file_path=temp_picture,
    )
    page.submit()

    result_text = page.get_result_table_text()

    assert "Иван Петров" in result_text
    assert "ivan.petrov@example.com" in result_text
    assert "Male" in result_text
    assert "9991234567" in result_text
    assert "25 Dec 1995" in result_text
    assert "Computer Science" in result_text
    assert "Sports, Music" in result_text
    assert "test_image.jpg" in result_text
    assert "NCR Delhi" in result_text


# Триангуляция: validateForm() на странице проверяет ровно 4 вещи —
# firstName, lastName, gender, 10-значный phone. Гоняем каждую из них
# по очереди как "невалидную", остальные оставляем корректными.
#
# ВАЖНО: сценарий "телефон длиннее 10 цифр" сюда не входит — у поля
# userNumber стоит HTML-атрибут maxlength="10", браузер физически не
# даёт ввести 11-й символ (как и живой человек с клавиатуры), поэтому
# JS-валидация до такого случая никогда не доходит. Это проверяется
# отдельным тестом ниже — test_phone_field_respects_maxlength.
@pytest.mark.parametrize(
    "first_name, last_name, gender, phone, case_name",
    [
        ("", "Петров", True, "9991234567", "пустое имя"),
        ("Иван", "", True, "9991234567", "пустая фамилия"),
        ("Иван", "Петров", False, "9991234567", "не выбран пол"),
        ("Иван", "Петров", True, "12345", "телефон короче 10 цифр"),
        ("Иван", "Петров", True, "", "пустой телефон"),
        ("Иван", "Петров", True, "abcdefghij", "телефон не из цифр"),
    ],
)
def test_required_field_validation(driver, first_name, last_name, gender, phone, case_name):
    page = RegistrationPage(driver).open()
    page.close_promo_banner_if_present()
    page.fill_required_fields(first_name, last_name, gender, phone)
    page.submit()

    error_text = page.get_form_error_text()
    assert "Please fill required fields" in error_text, (
        f"Сценарий '{case_name}': ожидалась ошибка валидации, получено: '{error_text}'"
    )


def test_phone_field_respects_maxlength(driver):
    """Поле телефона имеет maxlength=10 — проверяем, что браузер реально
    обрезает ввод до 10 символов, а не просто понадеемся на JS-валидацию."""
    page = RegistrationPage(driver).open()
    page.close_promo_banner_if_present()

    phone_field = driver.find_element(*RegistrationPage.PHONE)
    phone_field.send_keys("99912345678")  # 11 цифр

    assert phone_field.get_attribute("value") == "9991234567", (
        "Ожидалось, что maxlength=10 обрежет ввод до 10 символов"
    )