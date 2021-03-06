# Generated by Django 2.2.7 on 2019-11-29 11:44

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0015_auto_20191129_1118'),
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceTracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('account', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='expense.Account')),
            ],
        ),
    ]
