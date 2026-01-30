from selenium.webdriver.common.by import By


class HeaderPageLocators:
    # локатор верхней кнопки «Заказать»
    ORDER_BTN_TOP = (By.CLASS_NAME, "Button_Button__ra12g")
    # локатор логотипа Яндекса
    LOGO = (By.CLASS_NAME, "Header_Logo__23yGT")
