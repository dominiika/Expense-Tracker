# Generated by Django 2.2.7 on 2019-11-28 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0011_auto_20191128_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='initial_balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6),
        ),
    ]
