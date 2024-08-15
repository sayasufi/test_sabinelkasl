# Generated by Django 5.1 on 2024-08-15 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Наименование')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость')),
            ],
        ),
    ]
