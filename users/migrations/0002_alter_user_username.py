# Generated by Django 4.1.5 on 2023-09-13 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='Введите логин', max_length=150, verbose_name='логин'),
        ),
    ]
