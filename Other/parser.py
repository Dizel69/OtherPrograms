import httpx
import xml.etree.ElementTree as ET
import json

# URL для запроса данных
SIMBAD_URL = "https://simbad.cds.unistra.fr/simbad/sim-id?output.format=VOTable&Ident=M31"

def fetch_xml_data(url: str) -> str:
    """
    Делает GET-запрос и возвращает XML-данные как строку.
    """
    try:
        response = httpx.get(url)
        response.raise_for_status()
        return response.text
    except httpx.RequestError as e:
        print(f"Ошибка при запросе: {e}")
        return ""
    except httpx.HTTPStatusError as e:
        print(f"Ошибка HTTP-статуса: {e}")
        return ""

def parse_votable(xml_data: str) -> dict:
    """
    Парсит VOTable XML и извлекает данные.
    """
    try:
        # Пространство имён VOTable
        namespaces = {"v": "http://www.ivoa.net/xml/VOTable/v1.2"}
        root = ET.fromstring(xml_data)

        # Ищем таблицу с данными
        table = root.find(".//v:TABLE", namespaces)
        if table is None:
            return {"error": "No TABLE element found in XML"}

        # Извлекаем имена колонок
        fields = [field.attrib["name"] for field in table.findall("v:FIELD", namespaces)]

        # Извлекаем данные из <TABLEDATA>
        tabledata = table.find(".//v:TABLEDATA", namespaces)
        if tabledata is None:
            return {"error": "No TABLEDATA element found in XML"}

        rows = tabledata.findall("v:TR", namespaces)
        if not rows:
            return {"error": "No data rows found in XML"}

        # Парсим первую строку (TR)
        first_row = rows[0]
        result = {}
        for i, cell in enumerate(first_row.findall("v:TD", namespaces)):
            if i < len(fields):  # Защита от лишних данных
                result[fields[i]] = try_parse_number(cell.text)

        return result

    except ET.ParseError as e:
        return {"error": f"XML Parse Error: {e}"}

def try_parse_number(value: str):
    """
    Пробует преобразовать строку в число (float), если возможно.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return value

def main():
    """
    Главная функция: получает XML, парсит и выводит JSON.
    """
    print("Получаем данные...")
    xml_data = fetch_xml_data(SIMBAD_URL)

    if not xml_data:
        print("Не удалось получить XML.")
        return

    print("Парсим данные...")
    parsed_data = parse_votable(xml_data)

    # Сохраняем результат в JSON-файл
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=4, ensure_ascii=False)

    print("Готово! Результат сохранён в 'output.json'.")
main()