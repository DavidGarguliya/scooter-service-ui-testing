import allure

from pages.base_page import BasePage
from settings import DEFAULT_TIMEOUT
from locators.header_page_locators import HeaderPageLocators as Loc


class HeaderPage(BasePage):
    # ожидаем появления логотипа как признака загрузки шапки
    @allure.step("Дождаться загрузки хедера")
    def wait_for_load(self, timeout = DEFAULT_TIMEOUT):
        allure.attach(
            "Ждём появления логотипа Яндекса как индикатора готовности шапки.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        self.wait_visible(Loc.LOGO, timeout)

    # кликаем по верхней кнопке «Заказать»
    @allure.step("Нажать кнопку «Заказать» в хедере")
    def click_order_top(self, timeout = DEFAULT_TIMEOUT):
        allure.attach(
            "Нажимаем верхнюю кнопку заказа из шапки сайта.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        self.click(Loc.ORDER_BTN_TOP)
        
