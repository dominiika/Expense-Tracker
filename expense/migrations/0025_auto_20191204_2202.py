# Generated by Django 2.2.7 on 2019-12-04 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0024_auto_20191129_1626'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='balancetracker',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='income',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='spending',
            options={'ordering': ['-date']},
        ),
    ]