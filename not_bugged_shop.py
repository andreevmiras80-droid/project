import json
from pathlib import Path

import numpy as np  # ОШИБКА №1 в твоём коде: np не был импортирован


def load_shop(path: Path):
    """Читает shop.json и возвращает три массива NumPy: names, prices, sold.

    Функция ТОЛЬКО загружает и проверяет данные. Считать и печатать - не её дело.
    """
    # --- 1. Чтение файла: переводим системные ошибки в понятные, сохраняя причину (from e)
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Файл не найден: {path}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Некорректный JSON в {path}: {e}") from e

    # --- 2. Проверяем СТРУКТУРУ: сверху словарь, внутри ключа "products" непустой список
    # ОШИБКА №2 в твоём коде: ты искал "name", "price", "sold" на верхнем уровне,
    # а они лежат ВНУТРИ каждого товара из списка data["products"].
    if not isinstance(data, dict):
        raise ValueError("Верхний уровень JSON должен быть словарём")

    products = data.get("products")
    if not isinstance(products, list) or not products:
        raise ValueError("Ключ 'products' должен быть непустым списком")

    # --- 3. Проходим по товарам и собираем три обычных списка
    names, prices, sold = [], [], []
    for i, item in enumerate(products):
        if not isinstance(item, dict):
            raise ValueError(f"Товар №{i} должен быть словарём, а не {type(item).__name__}")

        for key in ("name", "price", "sold"):
            if key not in item:
                raise ValueError(f"У товара №{i} нет ключа '{key}'")

        for key in ("price", "sold"):
            if not isinstance(item[key], (int, float)):
                raise ValueError(f"У товара №{i} поле '{key}' должно быть числом, а не {item[key]!r}")

        names.append(item["name"])
        prices.append(item["price"])
        sold.append(item["sold"])

    # --- 4. Превращаем в массивы NumPy.
    # ОШИБКА №3 в твоём коде: prices * sold на обычных списках Python не работает (TypeError).
    return np.array(names), np.array(prices), np.array(sold)


def main():
    names, prices, sold = load_shop(Path("shop.json"))
    print("Формы:", names.shape, prices.shape, sold.shape)  # (6,) (6,) (6,)

    # Выручка: поэлементное умножение, цикл не нужен
    revenue = prices * sold
    print("Общая выручка:", revenue.sum())

    # Самый продаваемый ПО ШТУКАМ: argmax(sold), а не argmax(revenue).
    # argmax возвращает ОДНО число - индекс, поэтому `for x in np.argmax(...)` не работает.
    best = np.argmax(sold)
    print(f"Самый продаваемый: {names[best]} ({sold[best]} шт.)")

    # Сортировка по выручке по убыванию:
    # argsort даёт индексы по возрастанию, [::-1] разворачивает порядок.
    # names - массив NumPy, поэтому им можно индексировать массивом индексов.
    order = np.argsort(revenue)[::-1]
    print("По выручке (убывание):")
    for name, rev in zip(names[order], revenue[order]):
        print(f"  {name}: {rev}")


main()