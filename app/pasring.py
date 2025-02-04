import requests
import json
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Referer": "https://dom.mosreg.ru/uk"
}

all_companies = []


def parse_page(url):
    """ Функция для парсинга страницы dom.mosreq.ru """
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return None

    data = response.json()
    if "eias_uk_list" not in data:
        return None

    soup = BeautifulSoup(data["eias_uk_list"], "lxml")
    companies = soup.select("div.data-list-item a")

    results = []
    for company in companies:
        name = company.text.strip()
        link = "https://dom.mosreg.ru" + company["href"]
        index = company["href"].rfind('/') + 1
        id = company["href"][index:]
        results.append({"name": name, "link": link, 'id': id})

    return results


# Запуск с нулевой страницы
main_page_data = parse_page("https://dom.mosreg.ru/eias/uk/reestr")
if main_page_data:
    all_companies.extend(main_page_data)

# Запуск со страницей с пагинацией
page = 1
while True:
    url = f"https://dom.mosreg.ru/eias/uk/reestr?page={page}"
    print(f"Обрабаботка {page} страницы")
    page_data = parse_page(url)

    if not page_data:
        break  # Если данных больше нет, останавливаемся

    all_companies.extend(page_data)
    page += 1  # Следующая страница

# Сохраняем результат в JSON
with open("managing_companies.json", "w", encoding="utf-8") as file:
    json.dump(all_companies, file, ensure_ascii=False, indent=4)

print(f"Всего собрано {len(all_companies)} компаний, сохранено в managing_companies.json")
