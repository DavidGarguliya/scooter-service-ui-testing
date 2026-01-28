from selenium.webdriver.common.by import By


class OrderPageLocators:
    # Шаг 1 — данные пользователя
    INPUT_NAME = (By.XPATH, "//input[@placeholder='* Имя']")
    INPUT_SURNAME = (By.XPATH, "//input[@placeholder='* Фамилия']")
    INPUT_ADDRESS = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    INPUT_METRO = (By.XPATH, "//input[@placeholder='* Станция метро']")
    METRO_OPTION = (By.XPATH, "//div[contains(@class,'select-search__select')]//div[text()='{}']")
    INPUT_PHONE = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    BUTTON_NEXT = (By.XPATH, "//button[text()='Далее']")

    # Шаг 2 — детали аренды
    INPUT_DATE = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    DROPDOWN_DURATION = (By.XPATH, "//div[contains(@class,'Dropdown-control')]")
    OPTION_DURATION = (By.XPATH, "//div[contains(@class,'Dropdown-menu')]/div[text()='{}']")
    CHECKBOX_BLACK = (By.ID, "black")
    CHECKBOX_GREY = (By.ID, "grey")
    INPUT_COMMENT = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
    BUTTON_ORDER = (By.XPATH, "//button[contains(@class,'Button_Middle__1CSJM') and text()='Заказать']")
    BUTTON_CONFIRM_YES = (By.XPATH, "//button[text()='Да']")
    MODAL_HEADER = (By.XPATH, "//div[contains(@class,'Order_ModalHeader')]")

    # Логотипы в хедере
    LOGO_SCOOTER = (By.CLASS_NAME, "Header_LogoScooter__3lsAR")
    LOGO_YANDEX = (By.CLASS_NAME, "Header_LogoYandex__3TSOI")
