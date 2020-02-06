from django.test import TestCase
from expense.forms import AccountModelForm, IncomeModelForm, SpendingModelForm
from expense.models import Currency


class TestForms(TestCase):

    def test_account_model_form_valid_data(self):

        currency = Currency.objects.create(name='PLN')
        form = AccountModelForm(data={
            'current_balance': 2000,
            'currency': str(currency.id)
        })

        self.assertTrue(form.is_valid())

    def test_account_model_form_no_data(self):
        form = AccountModelForm(data={})

        self.assertFalse(form.is_valid())

    def test_income_model_form_valid_data(self):
        form = IncomeModelForm(data={
            'title': 'salary',
            'amount': 3000
        })

        self.assertTrue(form.is_valid())

    def test_income_model_form_no_data(self):
        form = IncomeModelForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_spending_model_form_valid_data(self):
        form = SpendingModelForm(data={
            'title': 'food',
            'amount': 100
        })

        self.assertTrue(form.is_valid())

    def test_spending_model_form_no_data(self):
        form = SpendingModelForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)
