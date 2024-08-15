import os
from io import BytesIO
import logging
from datetime import datetime
from collections import Counter

import pdfkit
import qrcode
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Item
from .serializers import ItemSerializer

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@api_view(['POST'])
def generate_receipt(request) -> JsonResponse:
    """
    Обрабатывает POST-запрос для генерации чека в формате PDF.

    Параметры:
        request (HttpRequest): HTTP-запрос, содержащий JSON с массивом идентификаторов товаров.

    Возвращает:
        JsonResponse: JSON-ответ, содержащий ссылку на PDF-файл и QR-код.
    """
    try:
        # Получаем список id товаров из запроса
        item_ids = request.data.get('items', [])
        logger.info(f"Получены id товаров: {item_ids}")

        # Подсчитываем количество каждого id
        item_counts = Counter(item_ids)
        logger.info(f"Подсчитано количество каждого товара: {item_counts}")

        # Получаем товары из базы данных
        items = Item.objects.filter(id__in=item_counts.keys())
        logger.info(f"Товары из базы данных: {[item.title for item in items]}")

        # Вычисляем общую сумму и подготавливаем данные для отображения
        total_sum = 0
        receipt_items = []
        for item in items:
            count = item_counts[item.id]
            total_price = item.price * count
            total_sum += total_price
            receipt_items.append({
                'title': item.title,
                'count': count,
                'price': item.price,
                'total_price': total_price
            })
        logger.info(f"Общая сумма: {total_sum}, Детали чека: {receipt_items}")

        # Время создания чека
        created_at = datetime.now().strftime("%d.%m.%Y %H:%M")
        logger.info(f"Время создания чека: {created_at}")

        # Рендерим HTML-шаблон чека с использованием Jinja2
        html = render_to_string('receipt_template.html', {
            'items': receipt_items,
            'total_sum': total_sum,
            'created_at': created_at
        })
        logger.info("HTML-шаблон чека успешно отрендерен.")

        # Генерация PDF из HTML
        pdf_path = os.path.join(settings.MEDIA_ROOT, f"receipt_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")
        pdfkit.from_string(html, pdf_path)
        logger.info(f"PDF успешно сгенерирован по пути: {pdf_path}")

        # Генерация QR-кода
        qr_code_img = qrcode.make(f"http://{request.get_host()}/media/{os.path.basename(pdf_path)}")
        qr_code_io = BytesIO()
        qr_code_img.save(qr_code_io)  # Убираем аргумент 'format'
        qr_code_path = os.path.join(settings.MEDIA_ROOT, f"qr_{datetime.now().strftime('%Y%m%d%H%M%S')}.png")
        with open(qr_code_path, 'wb') as qr_code_file:
            qr_code_file.write(qr_code_io.getvalue())
        logger.info(f"QR-код успешно сгенерирован по пути: {qr_code_path}")

        # Возвращаем ответ с QR-кодом и ссылкой на PDF
        return JsonResponse({
            'pdf_url': f"/media/{os.path.basename(pdf_path)}",
            'qr_code_url': f"/media/{os.path.basename(qr_code_path)}"
        })

    except Exception as e:
        logger.error(f"Произошла ошибка при генерации чека: {e}")
        return JsonResponse({'error': 'Ошибка при генерации чека'}, status=500)


@api_view(['GET'])
def get_all_items(request) -> Response:
    """
    Возвращает список всех товаров с их ID и наименованиями.

    Параметры:
        request (HttpRequest): HTTP-запрос.

    Возвращает:
        Response: JSON-ответ, содержащий список всех товаров с их ID и наименованиями.
    """
    items = Item.objects.all()
    item_data = [{"id": item.id, "title": item.title} for item in items]

    return Response(item_data)