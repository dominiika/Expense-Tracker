from django.test import TestCase
from django.urls import reverse
from expense.models import Currency, Account, Income, BalanceTracker
from django.contrib.auth.models import User


class TestAccountViews(TestCase):

    def setUp(self):

        self.currency = Currency.objects.create(name='PLN')
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )
        self.client.login(username='testuser', password='password123')
        self.account = Account.objects.create(
            user=self.user,
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
            slug=self.initial_income.slug
        )

    def test_index_page_GET(self):
        url = reverse('index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'expense/index.html'
        )

    def test_create_account_GET(self):
        url = reverse('create-account')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'expense/create.html'
        )

    def test_create_account_POST(self):
        url = reverse('create-account')
        currency = Currency.objects.create(name='USD')
        response = self.client.post(url,
                                    {'user': str(self.user.id),
                                     'current_balance': 2000,
                                     'currency': str(currency.id),
                                     'initial_balance': 1000})

        account = Account.objects.get(currency=self.currency, user=self.user)
        initial_income = Income.objects.get(
            account=account,
            title="Initial balance"
        )
        balance_tracker = BalanceTracker.objects.get(
            slug=initial_income.slug,
            account=account
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(account)
        self.assertTrue(balance_tracker)

    def test_create_account_POST_already_exists(self):

        url = reverse('create-account')
        accounts_count = Account.objects.all().count()
        response = self.client.post(url,
                                    {'user': str(self.user.id),
                                     'current_balance': 2000,
                                     'currency': str(self.currency.id),
                                     'initial_balance': 1000})

        accounts_count_after_response = Account.objects.all().count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(accounts_count, accounts_count_after_response)

    def test_account_detail_GET(self):

        url = reverse('account-detail', args=[1])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'expense/account-detail.html'
        )

    def account_detail_divided_GET(self):

        url = reverse('account-detail-divided', args=[1])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'expense/account-detail-divided.html'
        )

    def test_delete_account_GET(self):

        url = reverse('delete-account', args=[1])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expense/delete.html')

    def test_delete_account_POST(self):

        url = reverse('delete-account', args=[1])

        response = self.client.post(url)
        exists = Account.objects.filter(pk=self.account.id)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(exists)

    def test_delete_account_POST_not_allowed(self):

        self.client.logout()

        url = reverse('delete-account', args=[1])

        response = self.client.post(url)
        exists = Account.objects.filter(pk=self.account.id)

        self.assertEqual(response.status_code, 302)  # redirected to login page
        self.assertTrue(exists)
