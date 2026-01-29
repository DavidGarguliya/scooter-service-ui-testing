import pytest
import allure

from test_data import Credentials, RentDetails
from settings import BASE_URL, DEFAULT_TIMEOUT


order_cases = [
    pytest.param(
        "top_button",
        "click_order_top",
        Credentials.credentials_1,
        RentDetails.rent_details_1,
        id="order-top",
    ),
    pytest.param(
        "bottom_button",
        "click_order_bottom",
        Credentials.credentials_2,
        RentDetails.rent_details_2,
        id="order-bottom",
    ),
]


@allure.feature("Order")
@allure.story("Позитивный сценарий заказа")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("entry_id, click_method, credentials, rent", order_cases)

def test_order_positive_flow(main_page, order_page, entry_id, click_method, credentials, rent):
    allure.dynamic.title(f"Позитивный заказ ({entry_id})")
    allure.description("Проходим позитивный сценарий заказа самоката через выбранную точку входа.")

    with allure.step("Открыть главную страницу"):
        allure.attach("Готовим старт: открываем главную и закрываем баннер cookies.", name="Описание шага",
                      attachment_type=allure.attachment_type.TEXT)
        main_page.open()
        main_page.wait_for_load()

    with allure.step(f"Нажать кнопку заказа ({entry_id})"):
        allure.attach("Запускаем оформление через указанную кнопку заказа.", name="Описание шага",
                      attachment_type=allure.attachment_type.TEXT)
        getattr(main_page, click_method)()

    with allure.step("Заполнить данные клиента"):
        allure.attach("Вводим персональные данные пользователя на шаге 1.", name="Описание шага",
                      attachment_type=allure.attachment_type.TEXT)
        order_page.fill_customer_form(credentials)

    with allure.step("Заполнить данные аренды и подтвердить заказ"):
        allure.attach("Указываем параметры аренды, цвет, комментарий и подтверждаем заказ.", name="Описание шага",
                      attachment_type=allure.attachment_type.TEXT)
        order_page.fill_rent_form(rent)

    with allure.step("Проверить успешное создание заказа"):
        allure.attach("Проверяем заголовок модалки: заказ должен быть оформлен.", name="Описание шага",
                      attachment_type=allure.attachment_type.TEXT)
        success_header = order_page.get_success_header()
        assert "Заказ оформлен" in success_header


@allure.feature("Header navigation")
@allure.story("Логотип Самоката ведет на главную")
@allure.severity(allure.severity_level.NORMAL)

def test_logo_scooter_redirects_to_home(main_page, order_page):
    allure.dynamic.title("Логотип Самоката возвращает на главную")
    allure.description("Проверяем переход на главную страницу по клику на логотип Самоката.")

    with allure.step("Открыть страницу заказа"):
        allure.attach("Выбираем верхнюю кнопку заказа и переходим на форму.", name="Описание шага",
                      attachment_type=allure.attachment_type.TEXT)
        main_page.open()
        main_page.wait_for_load()
        main_page.click_order_top()

    with allure.step("Кликнуть по логотипу Самоката"):
        allure.attach("Жмём на логотип в хедере.", name="Описание шага",
                      attachment_type=allure.attachment_type.TEXT)
        order_page.click_scooter_logo()

    with allure.step("Убедиться, что открыт главный экран"):
        allure.attach("Сверяем текущий URL с базовым адресом.", name="Описание шага",
                      attachment_type=allure.attachment_type.TEXT)
        order_page.wait_url_contains(BASE_URL, timeout=DEFAULT_TIMEOUT)
        assert order_page.current_url().startswith(BASE_URL)


@allure.feature("Header navigation")
@allure.story("Логотип Яндекса открывает Дзен в новой вкладке")
@allure.severity(allure.severity_level.NORMAL)

def test_logo_yandex_opens_dzen(main_page, order_page):
    allure.dynamic.title("Логотип Яндекса открывает Дзен")
    allure.description("Проверяем открытие Дзена в новой вкладке по клику на логотип.")

    with allure.step("Открыть страницу заказа"):
        allure.attach("Переходим на форму заказа через верхнюю кнопку.", name="Описание шага",
                      attachment_type=allure.attachment_type.TEXT)
        main_page.open()
        main_page.wait_for_load()
        main_page.click_order_top()

    with allure.step("Кликнуть по логотипу Яндекса"):
        allure.attach("Жмём на логотип Яндекса в хедере и ждём новую вкладку.", name="Описание шага",
                      attachment_type=allure.attachment_type.TEXT)
        before = order_page.get_window_handles()
        order_page.click_yandex_logo()
        order_page.switch_to_new_tab(before, timeout=DEFAULT_TIMEOUT)

    with allure.step("Переключиться на новую вкладку и проверить URL"):
        allure.attach("Переключаемся на новую вкладку и проверяем, что открыта главная Дзена.",
                      name="Описание шага", attachment_type=allure.attachment_type.TEXT)
        order_page.wait_url_contains("dzen", timeout=DEFAULT_TIMEOUT)
        assert "dzen" in order_page.current_url()
