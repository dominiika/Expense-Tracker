from django.contrib import admin
from .models import Account, Income, Spending, Currency, BalanceTracker


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_balance', 'initial_balance', 'currency')

    def get_queryset(self, request):
        queryset = super(AccountAdmin, self).get_queryset(request)
        queryset = queryset.order_by('user')
        return queryset


class BalanceTrackerAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'date', 'slug')

    def get_queryset(self, request):
        queryset = super(BalanceTrackerAdmin, self).get_queryset(request)
        queryset = queryset.order_by('account')
        return queryset


class IncomeAdmin(admin.ModelAdmin):
    list_display = ('account', 'title', 'date', 'amount', 'current_balance', 'slug')

    def get_queryset(self, request):
        queryset = super(IncomeAdmin, self).get_queryset(request)
        queryset = queryset.order_by('account')
        return queryset


class SpendingAdmin(admin.ModelAdmin):
    list_display = ('account', 'title', 'date', 'amount', 'current_balance', 'slug')

    def get_queryset(self, request):
        queryset = super(SpendingAdmin, self).get_queryset(request)
        queryset = queryset.order_by('account')
        return queryset


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def get_queryset(self, request):
        queryset = super(CurrencyAdmin, self).get_queryset(request)
        queryset = queryset.order_by('name')
        return queryset


admin.site.register(Account, AccountAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Spending, SpendingAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(BalanceTracker, BalanceTrackerAdmin)



