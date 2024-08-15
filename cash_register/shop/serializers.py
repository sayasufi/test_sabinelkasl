from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Item, используется для конвертации данных модели в JSON и обратно.
    """

    class Meta:
        model = Item
        fields = ['id', 'title', 'price']