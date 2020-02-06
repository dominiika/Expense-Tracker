from django.test import TestCase
from django.urls import reverse, resolve
from expense import views


class TestUrls(TestCase):

    def test_create_account_url_resolves(self):
        url = reverse('create-account')

        self.assertEqual(resolve(url).func, views.create_account)

    def test_account_detail_url_resolves(self):
        url = reverse('account-detail', args=[1])

        self.assertEqual(resolve(url).func, views.account_detail)

    def test_account_detail_divided_url_resolves(self):
        url = reverse('account-detail-divided', args=[1])

        self.assertEqual(resolve(url).func, views.account_detail_divided)

    def test_delete_account_url_resolves(self):

        url = reverse('delete-account', args=[1])

        self.assertEqual(resolve(url).func, views.delete_account)

    def test_create_income_url_resolves(self):
        url = reverse('create-income', args=[1])

        self.assertEqual(resolve(url).func, views.create_income)

    def test_update_income_url_resolves(self):

        url = reverse('update-income', kwargs={'a_id': 1, 'i_id': 1})

        self.assertEqual(resolve(url).func, views.update_income)

    def test_delete_income_url_resolves(self):
        url = reverse('delete-income', kwargs={'a_id': 1, 'i_id': 1})

        self.assertEqual(resolve(url).func, views.delete_income)

    def test_create_spending_url_resolves(self):
        url = reverse('create-spending', args=[1])

        self.assertEqual(resolve(url).func, views.create_spending)

    def test_update_spending_url_resolves(self):
        url = reverse('update-spending', kwargs={'a_id': 1, 's_id': 1})

        self.assertEqual(resolve(url).func, views.update_spending)

    def test_delete_spending_url_resolves(self):
        url = reverse('delete-spending', kwargs={'a_id': 1, 's_id': 1})

        self.assertEqual(resolve(url).func, views.delete_spending)
