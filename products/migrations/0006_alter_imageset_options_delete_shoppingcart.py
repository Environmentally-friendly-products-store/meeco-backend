# Generated by Django 4.1.5 on 2023-09-17 12:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0005_alter_category_options_alter_product_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="imageset",
            options={
                "ordering": ["id"],
                "verbose_name": "изображение к товару",
                "verbose_name_plural": "изображения к товарам",
            },
        ),
        migrations.DeleteModel(
            name="ShoppingCart",
        ),
    ]