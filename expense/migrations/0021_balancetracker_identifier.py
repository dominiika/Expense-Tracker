# Generated by Django 2.2.7 on 2019-11-29 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0020_remove_balancetracker_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='balancetracker',
            name='identifier',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]