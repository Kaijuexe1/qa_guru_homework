import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    drv = webdriver.Chrome()
    drv.maximize_window()

    yield drv

    drv.quit()
