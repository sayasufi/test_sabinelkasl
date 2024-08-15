from django.db import models


class Item(models.Model):
    """
    Модель для представления товара в магазине.

    Атрибуты:
        title (str): Наименование товара.
        price (Decimal): Стоимость товара с двумя десятичными знаками.
    """

    title: str = models.CharField(
        max_length=200,
        verbose_name="Наименование"
    )
    price: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость"
    )

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта Item.

        Returns:
            str: Наименование товара.
        """
        return self.title