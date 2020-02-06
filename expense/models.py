from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


class Currency(models.Model):
    name = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class Account(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='accounts'
    )
    current_balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    initial_balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        blank=True
    )

    def __str__(self):
        return '{0.user} - {0.currency}'.format(self)


class Income(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        default=0,
        related_name='incomes'
    )
    date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    current_balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        default=0
    )
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    info = models.CharField(max_length=10, blank=True, default="Income")

    def _get_unique_slug(self):
        slug = str('income-')+slugify(self.title)
        unique_slug = slug
        num = 1
        while Income.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date', ]

    def date_short(self):
        return self.date.strftime('%-d %b %Y %H:%M:%S')


class Spending(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, default=0)
    date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    current_balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True, default=0
    )
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    info = models.CharField(max_length=10, blank=True, default="Spending")

    def _get_unique_slug(self):
        slug = str('spending-')+slugify(self.title)
        unique_slug = slug
        num = 1
        while Spending.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date', ]

    def date_short(self):
        return self.date.strftime('%-d %b %Y %H:%M:%S')


class BalanceTracker(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, default=0)
    date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ['-date', ]
