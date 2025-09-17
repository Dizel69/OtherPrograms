import json
import csv
import random

# путь к твоему json-файлу
INPUT_FILE = "main.json"
OUTPUT_FILE = "catalog.csv"

def parse_categories(categories, results, parents=None):
    """
    Рекурсивный парсер категорий с сохранением вложенности.
    """
    if parents is None:
        parents = []

    for cat in categories:
        name = cat.get("name", "").strip()
        if not name:
            continue

        # формируем полное имя: Родитель. Ребенок. Внук
        full_name = ". ".join(parents + [name])

        url = cat.get("url", "")
        if url.startswith("/"):
            url = "https://www.wildberries.ru" + url

        # добавляем запись
        results.append({
            "name": full_name,
            "url": url,
            "sku": 0,
            "priority": random.randint(1, 4)
        })

        # рекурсивно обходим детей
        if "childs" in cat and isinstance(cat["childs"], list):
            parse_categories(cat["childs"], results, parents + [name])


def main():
    # читаем JSON
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []
    parse_categories(data, results)

    # пишем в CSV (разделитель — таб)
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["name", "url", "sku", "priority"], delimiter="\t")
        writer.writeheader()
        writer.writerows(results)

    print(f"Готово! Сохранено {len(results)} строк в {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
