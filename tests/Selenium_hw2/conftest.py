import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    drv = webdriver.Chrome()
    drv.maximize_window()
    drv.implicitly_wait(5)
    yield drv
    drv.quit()
