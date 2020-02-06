from django import forms
from .models import Account, Income, Spending


class AccountModelForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('current_balance', 'currency',)


class IncomeModelForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ('title', 'amount',)


class SpendingModelForm(forms.ModelForm):
    class Meta:
        model = Spending
        fields = ('title', 'amount',)
