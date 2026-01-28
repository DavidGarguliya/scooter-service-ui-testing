import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from test_data import Credentials, RentDetails
from settings import BASE_URL


order_cases = [
    ("top_button", Credentials.credentials_1, RentDetails.rent_details_1),
    ("bottom_button", Credentials.credentials_2, RentDetails.rent_details_2),
]


@allure.feature("Order")
@allure.story("Позитивный сценарий заказа")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("entry_point, credentials, rent", order_cases, ids=["order-top", "order-bottom"])
def test_order_positive_flow(main_page, order_page, entry_point, credentials, rent):
    allure.dynamic.title(f"Позитивный заказ ({entry_point})")
    allure.description("Проходим позитивный сценарий заказа самоката через выбранную точку входа.")

    with allure.step("Открыть главную страницу"):
        allure.attach("Готовим старт: открываем главную и закрываем баннер cookies.", name="Описание шага",
                      attachment_type=allure.attachment_type.TEXT)
        main_page.open()
        main_page.wait_for_load()
        main_page.accept_cookies()

    with allure.step(f"Нажать кнопку заказа ({entry_point})"):
        allure.attach("Запускаем оформление через верхнюю или нижнюю кнопку заказа.", name="Описание шага",
                      attachment_type=allure.attachment_type.TEXT)
        if entry_point == "top_button":
            main_page.click_order_top()
        else:
            main_page.click_order_bottom()

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
def test_logo_scooter_redirects_to_home(main_page, order_page, driver):
    allure.dynamic.title("Логотип Самоката возвращает на главную")
    allure.description("Проверяем переход на главную страницу по клику на логотип Самоката.")

    with allure.step("Открыть страницу заказа"):
        allure.attach("Выбираем верхнюю кнопку заказа и переходим на форму.", name="Описание шага",
                      attachment_type=allure.attachment_type.TEXT)
        main_page.open()
        main_page.wait_for_load()
        main_page.accept_cookies()
        main_page.click_order_top()

    with allure.step("Кликнуть по логотипу Самоката"):
        allure.attach("Жмём на логотип в хедере.", name="Описание шага",
                      attachment_type=allure.attachment_type.TEXT)
        order_page.click_scooter_logo()

    with allure.step("Убедиться, что открыт главный экран"):
        allure.attach("Сверяем текущий URL с базовым адресом.", name="Описание шага",
                      attachment_type=allure.attachment_type.TEXT)
        WebDriverWait(driver, 5).until(EC.url_contains(BASE_URL))
        assert driver.current_url.startswith(BASE_URL)


@allure.feature("Header navigation")
@allure.story("Логотип Яндекса открывает Дзен в новой вкладке")
@allure.severity(allure.severity_level.NORMAL)
def test_logo_yandex_opens_dzen(main_page, order_page, driver):
    allure.dynamic.title("Логотип Яндекса открывает Дзен")
    allure.description("Проверяем открытие Дзена (или редиректа на ya.ru/yandex) в новой вкладке по клику на логотип.")

    with allure.step("Открыть страницу заказа"):
        allure.attach("Переходим на форму заказа через верхнюю кнопку.", name="Описание шага",
                      attachment_type=allure.attachment_type.TEXT)
        main_page.open()
        main_page.wait_for_load()
        main_page.accept_cookies()
        main_page.click_order_top()

    with allure.step("Кликнуть по логотипу Яндекса"):
        allure.attach("Жмём на логотип Яндекса в хедере и ждём новую вкладку.", name="Описание шага",
                      attachment_type=allure.attachment_type.TEXT)
        before = driver.window_handles.copy()
        order_page.click_yandex_logo()
        WebDriverWait(driver, 10).until(EC.new_window_is_opened(before))

    with allure.step("Переключиться на новую вкладку и проверить URL"):
        allure.attach("Переключаемся на новую вкладку и проверяем, что открыта главная Яндекса/Дзена.",
                      name="Описание шага", attachment_type=allure.attachment_type.TEXT)
        new_handle = [h for h in driver.window_handles if h not in before][0]
        driver.switch_to.window(new_handle)
        WebDriverWait(driver, 15).until(EC.url_matches(r"(dzen|ya\\.ru|yandex)"))
        assert any(k in driver.current_url for k in ["dzen", "ya.ru", "yandex"])
