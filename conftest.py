import os

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from pages.header_page import HeaderPage
from pages.main_page import MainPage
from pages.order_page import OrderPage
from settings import BASE_URL


@pytest.fixture(scope="session")
def driver():
    # настраиваем браузер Firefox
    options = Options()
    # управление режимом через переменную окружения HEADLESS=true/false
    if os.getenv("HEADLESS", "true").lower() == "true":
        options.add_argument("--headless")
    options.add_argument("--width=1280")
    options.add_argument("--height=1024")
    # создаем экземпляр драйвера
    driver = webdriver.Firefox(options=options)
    # открываем базовый адрес сразу после старта
    driver.get(BASE_URL)
    yield driver
    # корректно закрываем браузер после завершения всех тестов
    driver.quit()


@pytest.fixture
def header_page(driver):
    # возвращаем объект страницы шапки
    return HeaderPage(driver, BASE_URL)


@pytest.fixture
def main_page(driver):
    # возвращаем объект главной страницы
    return MainPage(driver, BASE_URL)


@pytest.fixture
def order_page(driver):
    # возвращаем объект страницы заказа
    return OrderPage(driver, BASE_URL)
