import allure

from pages.base_page import BasePage
from settings import DEFAULT_TIMEOUT
from locators.main_page_locators import MainPageLocators as Loc
from selenium.common.exceptions import TimeoutException


class MainPage(BasePage):
    @allure.step("Дождаться загрузки главной страницы")
    def wait_for_load(self, timeout = DEFAULT_TIMEOUT):
        allure.attach(
            "Ждем появления верхней кнопки «Заказать» как признака загрузки главной страницы.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        self.wait_visible(Loc.ORDER_BTN_TOP, timeout)

    @allure.step("Нажать кнопку «Заказать» вверху")
    def click_order_top(self):
        allure.attach(
            "Используем верхнюю CTA-кнопку на главной странице для старта оформления заказа.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        self.click(Loc.ORDER_BTN_TOP)

    @allure.step("Нажать кнопку «Заказать» внизу")
    def click_order_bottom(self, timeout = DEFAULT_TIMEOUT):
        allure.attach(
            "Используем нижнюю CTA-кнопку в блоке FAQ для старта оформления заказа.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        self.scroll_into_view(Loc.ORDER_BTN_BOTTOM)
        self.click(Loc.ORDER_BTN_BOTTOM)

    @allure.step("Сформировать локатор вопроса FAQ по индексу {question_index}")
    def get_question_locator(self, question_index: int) -> tuple[str, str]:
        allure.attach(
            f"Строим локатор для заголовка вопроса FAQ №{question_index}.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        return (
            Loc.QUESTION_LOCATOR[0],
            Loc.QUESTION_LOCATOR[1].format(question_index)
        )

    @allure.step("Сформировать локатор ответа FAQ по индексу {answer_index}")
    def get_answer_locator(self, answer_index: int) -> tuple[str, str]:
        allure.attach(
            f"Строим локатор для блока ответа FAQ №{answer_index}.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        return (
            Loc.ANSWER_LOCATOR[0],
            Loc.ANSWER_LOCATOR[1].format(answer_index)
        )


    @allure.step("Открыть вопрос FAQ под номером {question_index}")
    def click_question(self, question_index: int, timeout = DEFAULT_TIMEOUT):
        allure.attach(
            f"Скроллим и кликаем по вопросу FAQ с индексом {question_index}.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        locator = self.get_question_locator(question_index)
        self.scroll_into_view(locator, timeout)
        self.click(locator, timeout)

    @allure.step("Получить текст ответа FAQ под номером {answer_index}")
    def get_answer_text(self, answer_index: int, timeout = DEFAULT_TIMEOUT) -> str:
        allure.attach(
            f"Читаем текст ответа для вопроса с индексом {answer_index}.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        locator = self.get_answer_locator(answer_index)
        return self.get_text(locator, timeout)
