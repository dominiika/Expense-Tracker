# Generated by Django 2.2.7 on 2019-11-28 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0013_auto_20191128_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spending',
            name='account',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='expense.Account'),
        ),
    ]
