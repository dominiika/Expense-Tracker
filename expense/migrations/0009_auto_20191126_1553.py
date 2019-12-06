# Generated by Django 2.2.7 on 2019-11-26 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0008_account_total_expense_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='total_expense_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6),
        ),
    ]