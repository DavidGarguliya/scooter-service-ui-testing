import pytest
import allure

from test_data import Questions


@allure.feature("FAQ")
@allure.story("Ответы соответствуют ТЗ")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("FAQ: вопрос #{question_index} соответствует ТЗ")
@allure.description("Кликаем по вопросам аккордеона и сверяем текст ответов с эталонными значениями ТЗ.")

@pytest.mark.parametrize("question_index, expected_answer", Questions.items)

def test_faq_answer_text(main_page, question_index, expected_answer):
    with allure.step("Открыть главную страницу"):
        allure.attach("Переходим на главную страницу сервиса для проверки FAQ.", name="Описание шага",
                      attachment_type=allure.attachment_type.TEXT)
        main_page.open() 

    with allure.step(f"Раскрыть вопрос #{question_index}"):
        allure.attach(f"Открываем вопрос под индексом {question_index} в списке FAQ.",
                      name="Описание шага", attachment_type=allure.attachment_type.TEXT)
        main_page.click_question(question_index) 

    with allure.step("Получить текст ответа"):
        allure.attach("Читаем текст появившегося ответа.", name="Описание шага",
                      attachment_type=allure.attachment_type.TEXT)
        answer_text = main_page.get_answer_text(question_index)

    with allure.step("Сравнить ответ с ожидаемым из ТЗ"):
        allure.attach("Проверяем точное совпадение текста ответа с эталоном из ТЗ.",
                      name="Описание шага", attachment_type=allure.attachment_type.TEXT)
        assert answer_text == expected_answer
