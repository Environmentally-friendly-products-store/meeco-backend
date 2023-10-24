# Generated by Django 4.1.5 on 2023-10-24 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="long_name",
            field=models.CharField(
                blank=True,
                help_text="Введите наименование",
                max_length=255,
                null=True,
                verbose_name="Наименование товара длинное",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="structure",
            field=models.TextField(
                blank=True,
                help_text="Введите состав",
                max_length=512,
                null=True,
                verbose_name="Состав",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="brand",
            field=models.ForeignKey(
                help_text="Введите производителя",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="brand",
                to="products.brand",
                verbose_name="Брэнд",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(
                help_text="Введите описание",
                max_length=1000,
                verbose_name="Описание товара",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(
                help_text="Введите наименование",
                max_length=50,
                verbose_name="Наименование товара короткое",
            ),
        ),
    ]