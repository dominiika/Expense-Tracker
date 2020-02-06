from django.test import TestCase
from django.urls import reverse
from expense.models import Currency, Account, Income, Spending, BalanceTracker
from django.contrib.auth.models import User


class TestSpendingViews(TestCase):

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

        self.spending = Spending.objects.create(
            title='Spending',
            account=self.account,
            amount=100
        )
        self.spending_balance_tracker = BalanceTracker.objects.create(
            account=self.account,
            amount=self.account.current_balance,
            slug=self.spending.slug
        )

    def test_create_spending_GET(self):

        url = reverse('create-spending', args=[1])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expense/form.html')

    def test_create_spending_POST(self):

        url = reverse('create-spending', args=[1])

        response = self.client.post(
            url,
            {
                'account': self.account,
                'title': 'Test Spending',
                'amount': 1000
            }
        )
        new_spending = Spending.objects.get(
            account=self.account,
            title='Test Spending'
        )
        balance_tracker = BalanceTracker.objects.get(
            account=self.account,
            slug=new_spending.slug
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(new_spending)
        self.assertTrue(balance_tracker)

    def test_update_spending_GET(self):

        url = reverse(
            'update-spending',
            kwargs={'a_id': self.account.id, 's_id': self.spending.id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expense/form.html')

    def test_update_spending_POST(self):

        url = reverse(
            'update-spending',
            kwargs={
                'a_id': self.account.id,
                's_id': self.spending.id
            })

        response = self.client.post(url, {
            'title': 'Test Spending',
            'account': str(self.account.id),
            'amount': 50
        })

        self.spending.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.spending.amount, 50)

    def test_delete_spending_GET(self):

        url = reverse(
            'delete-spending',
            kwargs={'a_id': self.account.id, 's_id': self.spending.id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expense/delete.html')

    def test_delete_spending(self):

        url = reverse(
            'delete-spending',
            kwargs={'a_id': self.account.id, 's_id': self.spending.id}
        )

        response = self.client.post(url)

        exists = Spending.objects.filter(
            title='Test Spending',
            account=self.account
        ).exists()

        self.assertEqual(response.status_code, 302)
        self.assertFalse(exists)
