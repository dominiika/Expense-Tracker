from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from expense.models import Account, Income, Spending, BalanceTracker, Currency


class AdminSiteTests(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='testmail@mail.com',
            password='testpass123'
        )
        self.client.force_login(self.admin_user)

        self.currency = Currency.objects.create(name='USD')
        self.account = Account.objects.create(
            user=self.admin_user,
            currency=self.currency,
            current_balance=2000
        )
        self.initial_income = Income.objects.create(
            account=self.account,
            current_balance=self.account.current_balance,
            info="Initial",
            title="Initial balance",
            amount=self.account.current_balance
        )
        self.balance_tracker = BalanceTracker.objects.create(
            account=self.account,
            amount=self.account.current_balance,
            slug=self.initial_income.slug,
        )

    def test_accounts_listed(self):
        url = reverse('admin:expense_account_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.account.user)
        self.assertContains(response, self.account.current_balance)
        self.assertContains(response, self.account.initial_balance)
        self.assertContains(response, self.account.currency)

    def test_balance_trackers_listed(self):
        url = reverse('admin:expense_balancetracker_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.balance_tracker.account)
        self.assertContains(response, self.balance_tracker.amount)
        # self.assertContains(response, self.balance_tracker.date)
        self.assertContains(response, self.balance_tracker.slug)

    def test_currencies_listed(self):
        url = reverse('admin:expense_currency_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.currency.name)

    def test_incomes_listed(self):
        income = Income.objects.create(
            title='Income',
            account=self.account,
            amount=100
        )
        url = reverse('admin:expense_income_changelist')
        response = self.client.get(url)

        self.assertContains(response, income.account)
        self.assertContains(response, income.title)
        # self.assertContains(response, income.date)
        self.assertContains(response, income.amount)
        self.assertContains(response, income.current_balance)
        self.assertContains(response, income.slug)

    def test_spendings_listed(self):
        spending = Spending.objects.create(
            title='Spending',
            account=self.account,
            amount=100
        )
        url = reverse('admin:expense_spending_changelist')
        response = self.client.get(url)

        self.assertContains(response, spending.account)
        self.assertContains(response, spending.title)
        # self.assertContains(response, spending.date)
        self.assertContains(response, spending.amount)
        self.assertContains(response, spending.current_balance)
        self.assertContains(response, spending.slug)
