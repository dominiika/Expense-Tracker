# Generated by Django 2.2.7 on 2019-11-29 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0017_auto_20191129_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balancetracker',
            name='slug',
            field=models.SlugField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='income',
            name='slug',
            field=models.SlugField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='spending',
            name='slug',
            field=models.SlugField(blank=True, max_length=100),
        ),
    ]
