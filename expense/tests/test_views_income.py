from django.test import TestCase
from django.urls import reverse
from expense.models import Currency, Account, Income, BalanceTracker
from django.contrib.auth.models import User


class TestIncomeViews(TestCase):

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

        self.income = Income.objects.create(
            title='Income',
            account=self.account,
            amount=100
        )
        self.income_balance_tracker = BalanceTracker.objects.create(
            account=self.account,
            amount=self.account.current_balance,
            slug=self.income.slug
        )

    def test_create_income_GET(self):

        url = reverse('create-income', args=[1])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expense/form.html')

    def test_create_income_POST(self):

        url = reverse('create-income', args=[1])

        response = self.client.post(
            url,
            {
                'account': self.account,
                'title': 'test income',
                'amount': 1000
            }
        )
        new_income = Income.objects.get(
            account=self.account,
            title='test income'
        )
        balance_tracker = BalanceTracker.objects.get(
            account=self.account,
            slug=new_income.slug
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(new_income)
        self.assertTrue(balance_tracker)

    def test_update_income_GET(self):

        url = reverse(
            'update-income',
            kwargs={'a_id': self.account.id, 'i_id': self.income.id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expense/form.html')

    def test_update_income_POST(self):

        url = reverse(
            'update-income',
            kwargs={
                'a_id': self.account.id,
                'i_id': self.income.id
            })

        response = self.client.post(url, {
            'title': 'Test Income',
            'account': str(self.account.id),
            'amount': 50
        })

        self.income.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.income.amount, 50)

    def test_delete_income_GET(self):

        url = reverse(
            'delete-income',
            kwargs={'a_id': self.account.id, 'i_id': self.income.id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expense/delete.html')

    def test_delete_income_POST(self):

        url = reverse(
            'delete-income',
            kwargs={'a_id': self.account.id, 'i_id': self.income.id}
        )

        response = self.client.post(url)

        exists = Income.objects.filter(
            title='Test Income',
            account=self.account
        ).exists()

        self.assertEqual(response.status_code, 302)
        self.assertFalse(exists)

    def test_delete_income_POST_not_allowed(self):

        self.client.logout()

        url = reverse(
            'delete-income',
            kwargs={'a_id': self.account.id, 'i_id': self.income.id}
        )

        response = self.client.post(url)
        exists = Income.objects.filter(pk=self.income.id)

        self.assertEqual(response.status_code, 302)  # redirected to login page
        self.assertTrue(exists)
