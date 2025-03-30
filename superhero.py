import requests
from typing import Optional


def get_tallest_hero(gender: str, has_work: bool) -> Optional[dict]:
    url = "https://akabab.github.io/superhero-api/api/all.json"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Failed to fetch superhero data")

    heroes = response.json()

    filtered_heroes = []
    for hero in heroes:
        hero_gender = hero.get("appearance", {}).get("gender", "").lower()
        hero_work = bool(hero.get("work", {}).get("occupation"))
        if hero_gender == gender.lower() and hero_work == has_work:
            height_values = hero.get("appearance", {}).get("height", ["0 cm", "0 cm"])
            try:
                height_cm = int(height_values[1].split(" ")[0])
                hero["height_cm"] = height_cm
                filtered_heroes.append(hero)
            except (ValueError, IndexError):
                continue

    if not filtered_heroes:
        return None

    tallest_hero = max(filtered_heroes, key=lambda h: h["height_cm"])

    return tallest_hero


"Для просмотра, что найдет функция"

# if __name__ == "__main__":
#     gender = "Male"
#     has_work = True
#     hero = get_tallest_hero(gender, has_work)
#
#     if hero:
#         print(f"Самый высокий {gender}-герой с работой: {hero['name']} ({hero['height_cm']} см)")
#     else:
#         print(f"Герой с полом {gender} и наличием работы: НЕ НАЙДЕН")
