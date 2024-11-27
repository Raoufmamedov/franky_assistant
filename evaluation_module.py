import matplotlib.pyplot as plt
from statistics import median
import requests


def evaluate_assistant(questions, get_answer_fn):
    """
    Тестирует работу ассистента, оценивая его ответы по 3-балльной шкале.

    :param questions: список вопросов для тестирования.
    :param get_answer_fn: функция для получения ответа от ассистента (принимает строку, возвращает строку).
    """
    results = {}
    print("=== Тестирование ассистента ===")
    print("Оцените ответы по шкале:\n1.0: Правильный ответ\n0.0: Ответ неинформативный\n-1.0: Ошибочный ответ")
    print("Введите 'q', чтобы завершить тестирование.")

    for question in questions:
        print(f"\nВопрос: {question}")
        answer = get_answer_fn(question)
        print(f"Ответ: {answer}")
        while True:
            try:
                rating = input("Введите оценку (-1.0, 0.0, 1.0): ")
                if rating.lower() == "q":
                    print("Тестирование завершено.")
                    return results
                rating = float(rating)
                if rating in [-1.0, 0.0, 1.0]:
                    results[answer] = rating
                    break
                else:
                    print("Оценка должна быть -1.0, 0.0 или 1.0.")
            except ValueError:
                print("Введите корректное число.")

    return results


def real_get_answer_fn(question):
    """
    Функция для получения ответа от ассистента через API.

    :param question: Вопрос пользователя (строка).
    :return: Ответ ассистента (строка).
    """
    try:
        response = requests.post("http://127.0.0.1:8000/query/", json={"query": question})
        response.raise_for_status()  # Проверить на ошибки HTTP
        data = response.json()
        results = data.get("results", [])
        return results[0] if results else "Ответ не найден."
    except Exception as e:
        return f"Ошибка при запросе: {str(e)}"

def display_results(results):
    """
    Отображает результаты тестирования.

    :param results: словарь с парами "ответ": "оценка".
    """
    scores = list(results.values())
    if not scores:
        print("Нет данных для отображения.")
        return

    # Гистограмма
    plt.hist(scores, bins=3, edgecolor='black', align='left')
    plt.xticks([-1.0, 0.0, 1.0], labels=["Ошибочный", "Неинформативный", "Правильный"])
    plt.title("Оценки ответов ассистента")
    plt.xlabel("Оценка")
    plt.ylabel("Количество")
    plt.show()

    # Медианная оценка
    print(f"Медианная оценка: {median(scores)}")

# Пример использования
if __name__ == "__main__":
    # def mock_get_answer_fn(question):
    #     # Пример: замените на реальную функцию получения ответа от ассистента
    #     return f"Ответ на вопрос: {question}"
    def mock_get_answer_fn(question):
        return real_get_answer_fn(question)


    questions = [
        "Что такое база знаний?",
        "Как загрузить PDF-файл в систему?",
    ]

    results = evaluate_assistant(questions, mock_get_answer_fn)
    display_results(results)
