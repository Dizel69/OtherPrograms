import json
import csv
import random

# путь к твоему json-файлу
INPUT_FILE = "main.json"
OUTPUT_FILE = "catalog.csv"

def parse_categories(categories, results):
    """
    Рекурсивный парсер категорий.
    """
    for cat in categories:
        name = cat.get("name", "")
        url = cat.get("url", "")

        # если url относительный — добавляем домен
        if url.startswith("/"):
            url = "https://www.wildberries.ru" + url

        # добавляем запись
        results.append({
            "name": name,
            "url": url,
            "sku": 0,
            "priority": random.randint(1, 4)
        })

        # рекурсивно обходим детей
        if "childs" in cat:
            parse_categories(cat["childs"], results)


def main():
    # читаем JSON
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []
    parse_categories(data, results)

    # пишем в CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["name", "url", "sku", "priority"], delimiter="\t")
        writer.writeheader()
        writer.writerows(results)

    print(f"Готово! Сохранено {len(results)} строк в {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
