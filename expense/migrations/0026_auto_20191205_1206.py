# Generated by Django 2.2.7 on 2019-12-05 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0025_auto_20191204_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='current_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='account',
            name='initial_balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='balancetracker',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='income',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='income',
            name='current_balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='spending',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='spending',
            name='current_balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20),
        ),
    ]
