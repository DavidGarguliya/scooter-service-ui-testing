from selenium.webdriver.common.by import By


class MainPageLocators:
    # верхняя кнопка «Заказать»
    ORDER_BTN_TOP = (By.CLASS_NAME, "Button_Button__ra12g")
    # нижняя кнопка «Заказать» в блоке FAQ
    ORDER_BTN_BOTTOM = (
        By.XPATH,
        "//button[contains(@class,'Button_Middle__1CSJM') and text()='Заказать']",
    )
    # кнопка принятия cookies (если появляется)
    COOKIE_ACCEPT = (By.ID, "rcc-confirm-button")
    # вопросы и ответы в секции FAQ (форматируем индексом)
    QUESTION_LOCATOR = (By.ID, "accordion__heading-{}")
    ANSWER_LOCATOR = (By.XPATH, ".//div[@id='accordion__panel-{}']/p")
