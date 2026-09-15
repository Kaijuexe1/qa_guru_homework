import pytest
from selenium.webdriver.common.by import By
from table_element import TableElement

URL = "https://the-internet.herokuapp.com/tables"

EXPECTED_HEADERS = ["Last Name", "First Name", "Email", "Due", "Web Site", "Action"]


@pytest.mark.parametrize("table_id", ["table1", "table2"])
def test_table_headers(driver, table_id):
    driver.get(URL)
    table = TableElement(driver, (By.ID, table_id))
    assert table.get_headers() == EXPECTED_HEADERS


# Триангуляция: один и тот же метод get_row_data гоняем по разным
# таблицам/строкам вместо копипасты отдельного if __main__ на каждый случай
@pytest.mark.parametrize(
    "table_id, row_index, expected_last_name",
    [
        ("table1", 0, "Smith"),
        ("table2", 1, "Bach"),
        ("table2", 2, "Doe"),
        ("table2", 3, "Conway"),
    ],
)
def test_row_contains_expected_person(driver, table_id, row_index, expected_last_name):
    driver.get(URL)
    table = TableElement(driver, (By.ID, table_id))
    row = table.get_row_data(row_index)
    assert expected_last_name in row


# То же самое для get_cell_value — собрали все точечные проверки
# из трёх исходных файлов в одну параметризованную таблицу данных
@pytest.mark.parametrize(
    "table_id, row_index, column_index, expected_value, column_name",
    [
        ("table1", 2, 3, "$100.00", "Due"),
        ("table1", 3, 2, "tconway@earthlink.net", "Email"),
        ("table1", 0, 4, "http://www.jsmith.com", "Web Site"),
        ("table2", 3, 1, "Tim", "First Name"),
        ("table2", 0, 4, "http://www.jsmith.com", "Web Site"),
        ("table2", 2, 3, "$100.00", "Due"),
    ],
)
def test_cell_value(driver, table_id, row_index, column_index, expected_value, column_name):
    driver.get(URL)
    table = TableElement(driver, (By.ID, table_id))
    actual = table.get_cell_value(row_index, column_index)
    assert actual == expected_value, (
        f"{table_id}, строка {row_index}, колонка '{column_name}': "
        f"ожидалось '{expected_value}', получено '{actual}'"
    )


def test_wrong_expected_value_is_actually_caught(driver):

    driver.get(URL)
    table = TableElement(driver, (By.ID, "table1"))

    actual_due_value = table.get_cell_value(row_index=2, column_index=3)  # реально "$100.00"
    wrong_expected_value = "$999.00"  # заведомо неверное значение

    with pytest.raises(AssertionError):
        assert actual_due_value == wrong_expected_value, (
            f"Ожидалось '{wrong_expected_value}', получено '{actual_due_value}'"
        )
