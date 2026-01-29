from settings import BASE_URL, DEFAULT_TIMEOUT
from selenium.webdriver.support.wait import WebDriverWait  # явные ожидания
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


# базовый класс для всех страниц
class BasePage:
    def __init__(self, driver, base_url: str = BASE_URL):
        self.driver = driver
        self.base_url = base_url

    # открыть базовый URL (или переданный в конструктор)
    def open(self):
        self.driver.get(self.base_url)

    # видимость элемента
    def wait_visible(self, locator: tuple[str, str], timeout = DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    # присутствие в DOM
    def wait_presence(self, locator: tuple[str, str], timeout = DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    # кликабельность
    def wait_clickable(self, locator: tuple[str, str], timeout = DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    # безопасный клик: обычный, при перекрытии — JS
    def click(self, locator: tuple[str, str], timeout = DEFAULT_TIMEOUT) -> None:
        element = self.wait_clickable(locator, timeout)
        try:
            element.click()
        except ElementClickInterceptedException:
            # докручиваем в центр и кликаем через JS, чтобы обойти перекрытие картинкой
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                element,
            )
            self.driver.execute_script("arguments[0].click();", element)

    # ввод текста
    def type(
        self,
        locator: tuple[str, str],
        text: str,
        clear: bool = True,
        timeout = DEFAULT_TIMEOUT,
    ) -> None:
        element = self.wait_visible(locator, timeout)
        if clear:
            element.clear()
        element.send_keys(text)

    # получить текст
    def get_text(self, locator: tuple[str, str], timeout = DEFAULT_TIMEOUT) -> str:
        return self.wait_visible(locator, timeout).text

    # проверить, виден ли элемент
    def is_visible(self, locator: tuple[str, str], timeout = DEFAULT_TIMEOUT) -> bool:
        try:
            self.wait_visible(locator, timeout)
            return True
        except TimeoutException:
            return False

    # проскроллить к элементу
    def scroll_into_view(self, locator: tuple[str, str], timeout = DEFAULT_TIMEOUT):
        element = self.wait_presence(locator, timeout)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element,
        )
        return element

    # получить текущий URL
    def current_url(self) -> str:
        return self.driver.current_url

    # список открытых вкладок/окон
    def get_window_handles(self) -> list[str]:
        return self.driver.window_handles.copy()

    # переключиться на новую вкладку, открывшуюся после before_handles
    def switch_to_new_tab(self, before_handles: list[str], timeout = DEFAULT_TIMEOUT) -> str:
        WebDriverWait(self.driver, timeout).until(EC.new_window_is_opened(before_handles))
        new_handle = [h for h in self.driver.window_handles if h not in before_handles][0]
        self.driver.switch_to.window(new_handle)
        return new_handle

    # ждать, пока URL будет содержать подстроку
    def wait_url_contains(self, text: str, timeout = DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(EC.url_contains(text))

    # ждать точного совпадения паттерна (regex)
    def wait_url_matches(self, pattern: str, timeout = DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(EC.url_matches(pattern))
