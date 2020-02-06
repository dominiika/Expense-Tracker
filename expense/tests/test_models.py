from django.test import TestCase
from expense.models import Currency, Account, Income,\
    Spending, BalanceTracker
from django.contrib.auth import get_user_model


class TestCurrencyModel(TestCase):

    def setUp(self):
        self.currency = Currency.objects.create(
            name='PLN'
        )

    def test_currency_string_representation(self):

        self.assertEqual(str(self.currency), self.currency.name)


class TestAccountModel(TestCase):

    def setUp(self):

        self.currency = Currency.objects.create(
            name='PLN'
        )
        self.user = get_user_model().objects.create_user(
            username='test-user',
            password='testpass123'
        )
        self.account = Account.objects.create(
            user=self.user,
            currency=self.currency,
            current_balance=2000,
        )

    def test_account_string_representation(self):

        name = '{0.user} - {0.currency}'.format(self.account)

        self.assertEqual(str(self.account), name)


class TestIncomeModel(TestCase):

    def setUp(self):

        self.currency = Currency.objects.create(
            name='PLN'
        )
        self.user = get_user_model().objects.create_user(
            username='test-user',
            password='testpass123'
        )
        self.account = Account.objects.create(
            user=self.user,
            currency=self.currency,
            current_balance=2000,
        )
        self.income = Income.objects.create(
            account=self.account,
            title='test',
            amount=100,
        )

    def test_income_get_unique_slug(self):

        income_with_same_title = Income.objects.create(
            account=self.account,
            title='test',
            amount=100,
        )

        self.assertNotEqual(
            self.income.slug,
            income_with_same_title.slug)

    def test_income_date_is_shortened(self):

        self.assertEqual(
            self.income.date.strftime('%-d %b %Y %H:%M:%S'),
            self.income.date_short()
        )


class TestSpendingModel(TestCase):

    def setUp(self):

        self.currency = Currency.objects.create(
            name='PLN'
        )
        self.user = get_user_model().objects.create_user(
            username='test-user',
            password='testpass123'
        )
        self.account = Account.objects.create(
            user=self.user,
            currency=self.currency,
            current_balance=2000,
        )
        self.spending = Spending.objects.create(
            account=self.account,
            title='test',
            amount=200,
        )

    def test_spending_get_unique_slug(self):

        spending_with_same_title = Spending.objects.create(
            account=self.account,
            title='test',
            amount=100,
        )

        self.assertNotEqual(
            self.spending.slug,
            spending_with_same_title.slug)

    def test_spending_date_is_shortened(self):

        self.assertEqual(
            self.spending.date.strftime('%-d %b %Y %H:%M:%S'),
            self.spending.date_short()
        )


class TestBalanceTrackerModel(TestCase):

    def setUp(self):

        self.currency = Currency.objects.create(
            name='PLN'
        )
        self.user = get_user_model().objects.create_user(
            username='test-user',
            password='testpass123'
        )
        self.account = Account.objects.create(
            user=self.user,
            currency=self.currency,
            current_balance=2000,
        )
        self.balance_tracker = BalanceTracker.objects.create(
            account=self.account,
            amount=self.account.current_balance,
        )

    def balance_tracker_string_representation(self):
        self.assertEqual(str(self.balance_tracker), self.balance_tracker.slug)
