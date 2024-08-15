import logging
import os
import sys

import django
import random
from django.db import connection
# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("Current PYTHONPATH:", sys.path)
print("Current DJANGO_SETTINGS_MODULE:", os.environ.get('DJANGO_SETTINGS_MODULE'))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Устанавливаем путь к настройкам Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cash_register.settings')

# Настройка окружения Django
django.setup()

from shop.models import Item


def populate_items(n=100):
    """
    Функция для автоматического добавления n товаров в таблицу Item.
    Параметры:
        n (int): Количество товаров для добавления.
    """
    try:
        # Удаление всех записей из таблицы
        Item.objects.all().delete()
        logger.info("Все существующие товары удалены из таблицы.")

        # Сброс последовательности идентификаторов
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE shop_item_id_seq RESTART WITH 1;")
        logger.info("Последовательность идентификаторов сброшена.")

        # Примеры названий товаров
        item_names = [
            "Хлеб", "Молоко", "Яблоко", "Сыр", "Мясо", "Курица", "Мука", "Сахар", "Чай", "Кофе",
            "Масло", "Сырок", "Йогурт", "Колбаса", "Макароны", "Рис", "Гречка", "Печенье", "Шоколад", "Чипсы",
            "Майонез", "Кетчуп", "Горчица", "Соль", "Перец", "Вода", "Сок", "Газировка", "Пицца", "Бургеры"
        ]

        # Добавление новых записей
        for _ in range(n):
            name = random.choice(item_names)
            price = round(random.uniform(10, 500), 2)  # Генерация случайной цены от 10 до 500 руб.
            item = Item(title=name, price=price)
            item.save()

        logger.info(f"Добавлено {n} товаров в таблицу Item.")
    except Exception as e:
        logger.error(f"Произошла ошибка при добавлении товаров: {e}")
        raise


if __name__ == "__main__":
    if os.environ.get('POPULATE_DB', 'False') == 'True':
        populate_items()
    else:
        logger.info("Заполнение базы данных пропущено, так как POPULATE_DB не установлено в True.")