# Generated by Django 2.2.7 on 2020-01-20 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0026_auto_20191205_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='account',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='incomes', to='expense.Account'),
        ),
    ]
