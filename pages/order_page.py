import allure
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage
from settings import DEFAULT_TIMEOUT
from locators.order_page_locators import OrderPageLocators as Loc


class OrderPage(BasePage):
    duration_map = {
        1: "сутки",
        2: "двое суток",
        3: "трое суток",
        4: "четверо суток",
        5: "пятеро суток",
        6: "шестеро суток",
        7: "семеро суток",
        8: "восьмеро суток",
    }

    # заполняем шаг 1 формы заказа
    @allure.step("Заполнить данные клиента")
    def fill_customer_form(self, data: dict, timeout: int = DEFAULT_TIMEOUT):
        allure.attach(
            "Вводим имя, фамилию, адрес, станцию метро и телефон, затем переходим на шаг деталей аренды.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        self.type(Loc.INPUT_NAME, data["name"], timeout=timeout)
        self.type(Loc.INPUT_SURNAME, data["surname"], timeout=timeout)
        self.type(Loc.INPUT_ADDRESS, data["address"], timeout=timeout)

        # станция метро: вводим текст и выбираем пункт из списка
        self.click(Loc.INPUT_METRO, timeout)
        self.type(Loc.INPUT_METRO, data["metro_station"], clear=True, timeout=timeout)
        metro_option = (Loc.METRO_OPTION[0], Loc.METRO_OPTION[1].format(data["metro_station"]))
        self.click(metro_option, timeout)

        self.type(Loc.INPUT_PHONE, data["phone_number"], timeout=timeout)
        self.click(Loc.BUTTON_NEXT, timeout)

    # заполняем шаг 2 формы заказа
    @allure.step("Заполнить данные аренды")
    def fill_rent_form(self, data: dict, timeout: int = DEFAULT_TIMEOUT):
        allure.attach(
            "Выбираем дату, срок аренды, цвет самоката и добавляем комментарий, затем подтверждаем заказ.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        # дата начала аренды
        self.type(Loc.INPUT_DATE, data["start_date"], timeout=timeout)
        self.wait_visible(Loc.INPUT_DATE, timeout).send_keys(Keys.ENTER)

        # срок аренды
        self.click(Loc.DROPDOWN_DURATION, timeout)
        duration_text = self.duration_map.get(data["duration"], f"{data['duration']} суток")
        option_locator = (Loc.OPTION_DURATION[0], Loc.OPTION_DURATION[1].format(duration_text))
        self.click(option_locator, timeout)

        # цвет самоката
        if data.get("color_black"):
            self.click(Loc.CHECKBOX_BLACK, timeout)
        if data.get("color_grey"):
            self.click(Loc.CHECKBOX_GREY, timeout)

        # комментарий
        if data.get("comment"):
            self.type(Loc.INPUT_COMMENT, data["comment"], timeout=timeout)

        # кнопка «Заказать» на шаге 2
        self.click(Loc.BUTTON_ORDER, timeout)
        # подтверждаем заказ во всплывающем окне
        self.click(Loc.BUTTON_CONFIRM_YES, timeout)

    # возвращаем текст заголовка окна успешного заказа
    @allure.step("Получить заголовок модалки успешного заказа")
    def get_success_header(self, timeout: int = DEFAULT_TIMEOUT) -> str:
        allure.attach(
            "Считываем заголовок окна подтверждения, чтобы убедиться в успешном оформлении.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        return self.get_text(Loc.MODAL_HEADER, timeout)

    # переход по логотипу Самоката
    @allure.step("Клик по логотипу Самоката")
    def click_scooter_logo(self, timeout: int = DEFAULT_TIMEOUT):
        allure.attach(
            "Жмём на логотип Самоката в шапке, чтобы вернуться на главную страницу.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        self.click(Loc.LOGO_SCOOTER, timeout)

    # переход по логотипу Яндекса (открывается новая вкладка)
    @allure.step("Клик по логотипу Яндекса")
    def click_yandex_logo(self, timeout: int = DEFAULT_TIMEOUT):
        allure.attach(
            "Жмём на логотип Яндекса в шапке; ожидаем открытие новой вкладки с Дзен/Яндекс.",
            name="Описание шага",
            attachment_type=allure.attachment_type.TEXT,
        )
        self.click(Loc.LOGO_YANDEX, timeout)
