# Generated by Django 2.2.7 on 2019-11-29 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0016_balancetracker'),
    ]

    operations = [
        migrations.AddField(
            model_name='balancetracker',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='income',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='spending',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
    ]