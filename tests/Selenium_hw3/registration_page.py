from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RegistrationPage:
    URL = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"

    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    EMAIL = (By.ID, "userEmail")
    GENDER_MALE = (By.CSS_SELECTOR, "label[for='gender-radio-1']")
    PHONE = (By.ID, "userNumber")
    DATE_INPUT = (By.ID, "dateOfBirthInput")
    MONTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__month-select")
    YEAR_SELECT = (By.CSS_SELECTOR, ".react-datepicker__year-select")
    SUBJECTS_INPUT = (By.ID, "subjectsInput")
    HOBBY_SPORTS = (By.CSS_SELECTOR, "label[for='hobbies-checkbox-1']")
    HOBBY_MUSIC = (By.CSS_SELECTOR, "label[for='hobbies-checkbox-3']")
    UPLOAD_PICTURE = (By.ID, "uploadPicture")
    CURRENT_ADDRESS = (By.ID, "currentAddress")
    STATE_TRIGGER = (By.ID, "state")
    CITY_TRIGGER = (By.ID, "city")
    DROPDOWN_FIRST_OPTION = (By.XPATH, '//*[@id="stateCity-wrapper"]/div[1]')
    SUBMIT_BUTTON = (By.ID, "submit")
    FORM_ERROR = (By.ID, "formError")
    MODAL_TITLE = (By.ID, "example-modal-sizes-title-lg")
    RESULT_TABLE = (By.CLASS_NAME, "table-responsive")
    CLOSE_BANNER = (By.CSS_SELECTOR, "#fixedban button[aria-label='Close']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)
        return self

    def _js_click(self, locator):

        element = self.driver.find_element(*locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();",
            element,
        )
        return element

    def close_promo_banner_if_present(self):

        banners = self.driver.find_elements(*self.CLOSE_BANNER)
        if banners:
            banners[0].click()
            self.wait.until(EC.invisibility_of_element(banners[0]))
        return self

    def fill_required_fields(self, first_name="", last_name="", gender=True, phone=""):

        if first_name:
            self.driver.find_element(*self.FIRST_NAME).send_keys(first_name)
        if last_name:
            self.driver.find_element(*self.LAST_NAME).send_keys(last_name)
        if gender:
            self._js_click(self.GENDER_MALE)
        if phone:
            self.driver.find_element(*self.PHONE).send_keys(phone)
        return self

    def fill_full_form(self, first_name, last_name, email, phone,
                        address, subject, temp_file_path):
        self.driver.find_element(*self.FIRST_NAME).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME).send_keys(last_name)
        self.driver.find_element(*self.EMAIL).send_keys(email)
        self._js_click(self.GENDER_MALE)
        self.driver.find_element(*self.PHONE).send_keys(phone)

        self.pick_date(month_value=11, year_value=1995, day_value=25)  # 25 Dec 1995

        subjects_input = self.driver.find_element(*self.SUBJECTS_INPUT)
        subjects_input.send_keys(subject)
        subjects_input.send_keys("\ue007")  # Keys.ENTER

        self._js_click(self.HOBBY_SPORTS)
        self._js_click(self.HOBBY_MUSIC)

        self.driver.find_element(*self.UPLOAD_PICTURE).send_keys(temp_file_path)
        self.driver.find_element(*self.CURRENT_ADDRESS).send_keys(address)

        self.select_state_and_city()
        return self

    def pick_date(self, month_value: int, year_value: int, day_value: int):
        self._js_click(self.DATE_INPUT)
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "react-datepicker__month-container")))

        from selenium.webdriver.support.ui import Select
        Select(self.driver.find_element(*self.MONTH_SELECT)).select_by_value(str(month_value))
        Select(self.driver.find_element(*self.YEAR_SELECT)).select_by_value(str(year_value))

        day_locator = (
            By.CSS_SELECTOR,
            f".react-datepicker__day--{day_value:03d}:not(.react-datepicker__day--outside-month)",
        )
        self.wait.until(EC.visibility_of_element_located(day_locator))
        self._js_click(day_locator)
        return self

    def select_state_and_city(self):

        self._js_click(self.STATE_TRIGGER)
        self.wait.until(EC.visibility_of_element_located(self.DROPDOWN_FIRST_OPTION))
        self._js_click(self.DROPDOWN_FIRST_OPTION)

        self._js_click(self.CITY_TRIGGER)
        self.wait.until(EC.visibility_of_element_located(self.DROPDOWN_FIRST_OPTION))
        self._js_click(self.DROPDOWN_FIRST_OPTION)
        return self

    def submit(self):
        self._js_click(self.SUBMIT_BUTTON)
        return self

    def get_form_error_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.FORM_ERROR)).text

    def get_result_table_text(self) -> str:
        self.wait.until(EC.visibility_of_element_located(self.MODAL_TITLE))
        return self.driver.find_element(*self.RESULT_TABLE).text