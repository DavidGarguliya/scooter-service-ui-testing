import allure

from pages.base_page import BasePage
from settings import DEFAULT_TIMEOUT
from locators.main_page_locators import MainPageLocators as Loc


class MainPage(BasePage):
    # ожидаем появление верхней кнопки как сигнала загрузки страницы
    @allure.step("Дождаться загрузки главной страницы")
    def wait_for_load(self, timeout: int = DEFAULT_TIMEOUT):
        allure.attach(
            "Ждем появления верхней кнопки «Заказать» как признака загрузки главной страницы.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        self.wait_visible(Loc.ORDER_BTN_TOP, timeout)

    # принимаем cookies, если баннер виден
    @allure.step("Принять cookies, если баннер виден")
    def accept_cookies(self, timeout: int = 2):
        allure.attach(
            "Если баннер cookies отображается, закрываем его, чтобы элементы не перекрывались.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        if self.is_visible(Loc.COOKIE_ACCEPT, timeout):
            self.click(Loc.COOKIE_ACCEPT, timeout)

    # кликаем по верхней кнопке «Заказать»
    @allure.step("Нажать кнопку «Заказать» вверху")
    def click_order_top(self, timeout: int = DEFAULT_TIMEOUT):
        allure.attach(
            "Используем верхнюю CTA-кнопку на главной странице для старта оформления заказа.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        self.click(Loc.ORDER_BTN_TOP, timeout)

    # прокручиваем к нижней кнопке «Заказать» и возвращаем элемент
    @allure.step("Прокрутить к нижней кнопке «Заказать»")
    def scroll_to_order_bottom(self, timeout: int = DEFAULT_TIMEOUT):
        allure.attach(
            "Скроллим страницу до нижней кнопки заказа, чтобы сделать её доступной для клика.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        return self.scroll_to(Loc.ORDER_BTN_BOTTOM, timeout)

    # кликаем по нижней кнопке «Заказать» (с автоскроллом)
    @allure.step("Нажать кнопку «Заказать» внизу")
    def click_order_bottom(self, timeout: int = DEFAULT_TIMEOUT):
        allure.attach(
            "Используем нижнюю CTA-кнопку в блоке FAQ для старта оформления заказа.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        self.scroll_to_order_bottom(timeout)
        self.click(Loc.ORDER_BTN_BOTTOM, timeout)

    # раскрываем вопрос в FAQ по индексу
    @allure.step("Открыть вопрос FAQ под номером {question_index}")
    def click_question(self, question_index: int, timeout: int = DEFAULT_TIMEOUT):
        allure.attach(
            f"Скроллим и кликаем по вопросу FAQ с индексом {question_index}.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        locator = (Loc.QUESTION_LOCATOR[0], Loc.QUESTION_LOCATOR[1].format(question_index))
        # ждём появления элемента в DOM
        element = self.wait_presence(locator, timeout)
        # скроллим к элементу с привязкой к верхней части окна
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'start'});", element)
        # поднимаем экран чуть выше, чтобы картинка самоката не перекрывала элемент
        self.driver.execute_script("window.scrollBy(0, -400);")
        # обычный click по элементу
        self.click(locator, timeout)

    # возвращаем текст ответа в FAQ по индексу
    @allure.step("Получить текст ответа FAQ под номером {answer_index}")
    def get_answer_text(self, answer_index: int, timeout: int = DEFAULT_TIMEOUT) -> str:
        allure.attach(
            f"Читаем текст ответа для вопроса с индексом {answer_index}.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        locator = (Loc.ANSWER_LOCATOR[0], Loc.ANSWER_LOCATOR[1].format(answer_index))
        return self.get_text(locator, timeout)
