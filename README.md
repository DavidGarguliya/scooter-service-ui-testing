# UI тесты для сервиса «Самокат»

Автотесты на Python + Pytest + Selenium WebDriver (Firefox) для проверки главной страницы и потока заказа самоката.

## Стек
- Python 3.14
- Pytest
- Selenium WebDriver (Firefox/Geckodriver)
- Allure для отчетов

## Установка
```bash
pip install -r requirements.txt
```

## Запуск тестов
- Все тесты (headless по умолчанию):
```bash
pytest --alluredir=allure-results
```
- Без headless:
```bash
HEADLESS=false pytest --alluredir=allure-results
```

## Allure-отчет
```bash
allure serve allure-results
# или
allure generate allure-results -o allure-report --clean
```

## Основные проверки
- FAQ: тексты ответов соответствуют ТЗ.
- Позитивный заказ самоката: два набора данных, две точки входа (верхняя/нижняя кнопка).
- Навигация по логотипам: Самокат → главная, Яндекс → Дзен/ya.ru/yandex в новой вкладке.

## Структура
- `pages/` — Page Object'ы.
- `locators/` — локаторы страниц.
- `tests/` — тестовые сценарии.
- `test_data.py` — тестовые данные для заказов и FAQ.
- `settings.py` — базовые настройки проекта.
