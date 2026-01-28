# импортируем тип Optional для аннотации необязательных аргументов
from typing import Optional
# импортируем класс WebDriverWait для работы с явными ожиданиями
from selenium.webdriver.support.wait import WebDriverWait
# импортируем набор готовых условий для ожиданий
from selenium.webdriver.support import expected_conditions as EC


# объявляем базовый класс для всех страниц проекта
class BasePage:
    # конструктор принимает драйвер и необязательный базовый адрес
    def __init__(self, driver, base_url: Optional[str] = None):
        # сохраняем экземпляр драйвера как поле объекта
        self.driver = driver
        # сохраняем базовый адрес, если он передан
        self.base_url = base_url

    # вспомогательный метод формирует полный URL из базового адреса и относительного пути
    def _make_url(self, path: str) -> str:
        # если базовый адрес задан и путь не является абсолютным URL
        if self.base_url and not path.startswith("http"):
            # возвращаем склеенный адрес без двойных слэшей
            return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        # иначе возвращаем исходный путь как есть
        return path

    # открываем страницу по относительному или абсолютному адресу
    def open(self, path: str = "") -> None:
        # передаем в драйвер итоговый URL для загрузки
        self.driver.get(self._make_url(path))

    # ждем, пока элемент станет видимым, и возвращаем его
    def wait_visible(self, locator: tuple[str, str], timeout: int = 5):
        # создаем объект ожидания с указанным таймаутом
        wait = WebDriverWait(self.driver, timeout)
        # дожидаемся видимости элемента по локатору
        return wait.until(EC.visibility_of_element_located(locator))

    # ждем, пока элемент появится в DOM, даже если он невидим
    def wait_presence(self, locator: tuple[str, str], timeout: int = 5):
        # создаем объект ожидания
        wait = WebDriverWait(self.driver, timeout)
        # дожидаемся присутствия элемента в дереве DOM
        return wait.until(EC.presence_of_element_located(locator))

    # ждем, пока элемент станет кликабельным, и возвращаем его
    def wait_clickable(self, locator: tuple[str, str], timeout: int = 5):
        # создаем объект ожидания
        wait = WebDriverWait(self.driver, timeout)
        # дожидаемся, что элемент кликабелен
        return wait.until(EC.element_to_be_clickable(locator))

    # возвращаем первый найденный видимый элемент
    def find(self, locator: tuple[str, str], timeout: int = 5):
        # используем метод ожидания видимости
        return self.wait_visible(locator, timeout)

    # возвращаем список всех найденных элементов без ожидания
    def find_all(self, locator: tuple[str, str]):
        # ищем элементы напрямую через драйвер
        return self.driver.find_elements(*locator)

    # кликаем по элементу, дожидаясь кликабельности
    def click(self, locator: tuple[str, str], timeout: int = 5) -> None:
        # получаем кликабельный элемент
        element = self.wait_clickable(locator, timeout)
        # вызываем событие клика
        element.click()

    # вводим текст в поле, при необходимости предварительно очищая его
    def type(self, locator: tuple[str, str], text: str, clear: bool = True, timeout: int = 5) -> None:
        # дожидаемся видимости элемента ввода
        element = self.wait_visible(locator, timeout)
        # очищаем поле, если это запрошено
        if clear:
            element.clear()
        # отправляем текст в элемент
        element.send_keys(text)

    # возвращаем текст видимого элемента
    def get_text(self, locator: tuple[str, str], timeout: int = 5) -> str:
        # дожидаемся видимости и берем текст
        return self.wait_visible(locator, timeout).text

    # проверяем, виден ли элемент за отведенное время, возвращая булево значение
    def is_visible(self, locator: tuple[str, str], timeout: int = 3) -> bool:
        # оборачиваем ожидание в блок try/except
        try:
            # пробуем дождаться видимости
            self.wait_visible(locator, timeout)
            # если ожидание успешно, возвращаем True
            return True
        # перехватываем исключение таймаута
        except Exception:
            # возвращаем False при отсутствии элемента
            return False

    # ждем, пока элемент исчезнет со страницы
    def wait_invisible(self, locator: tuple[str, str], timeout: int = 5) -> bool:
        # создаем объект ожидания
        wait = WebDriverWait(self.driver, timeout)
        # дожидаемся невидимости элемента и возвращаем результат
        return wait.until(EC.invisibility_of_element_located(locator))

    # прокручиваем страницу к элементу и возвращаем его
    def scroll_to(self, locator: tuple[str, str], timeout: int = 5):
        # дожидаемся присутствия элемента в DOM
        element = self.wait_presence(locator, timeout)
        # вызываем JavaScript, чтобы прокрутить к элементу
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        # возвращаем элемент, чтобы можно было с ним работать дальше
        return element

    # прокручиваем страницу в самый низ
    def scroll_to_bottom(self) -> None:
        # выполняем JavaScript для прокрутки к нижней границе документа
        self.driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")

    # прокручиваем страницу в самый верх
    def scroll_to_top(self) -> None:
        # выполняем JavaScript для прокрутки к верхней границе документа
        self.driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
