# Generated by Django 2.2.7 on 2019-11-26 13:03

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_balance', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Spending',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('title', models.CharField(max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('balance', models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='expense.Account')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spending_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('title', models.CharField(max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('balance', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='expense.Account')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='income_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense.Currency'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balance_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
