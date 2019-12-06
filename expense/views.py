from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Income, Spending, BalanceTracker
from .forms import AccountModelForm, IncomeModelForm, SpendingModelForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from chartit import DataPool, Chart


@login_required(login_url="/profile/login/")
def index(request):
    accounts = Account.objects.filter(user=request.user)

    context = {'accounts': accounts}
    return render(request, 'expense/index.html', context)


@login_required(login_url="/profile/login/")
def create_account(request):
    form = AccountModelForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        obj = form.save(commit=False)
        account = Account.objects.filter(currency=obj.currency, user=request.user)
        if account.exists():
            context['account'] = Account.objects.filter(currency=obj.currency, user=request.user)[0]
            message = f"You already have an account in this currency! Do you want to update existing account?"
            context['message'] = message
            return render(request, 'expense/create.html', context)
        else:
            obj.user = request.user
            obj.initial_balance = obj.current_balance
            obj.save()
            new_account = Account.objects.get(currency=obj.currency, user=request.user)
            income = Income.objects.create(account=new_account, current_balance=new_account.current_balance,
                                           info="Initial", title="Initial balance", amount=new_account.current_balance)
            income.save()

            balance_tracker = BalanceTracker.objects.create(account=new_account, amount=new_account.current_balance,
                                                            slug=income.slug)
        return redirect('/')
    return render(request, 'expense/create.html', context)


@login_required(login_url="/profile/login/")
def delete_account(request, a_id):
    account = get_object_or_404(Account, pk=a_id)
    if account.user == request.user:
        if request.method == 'POST':
            account.delete()
            return redirect('/')
        context = {'account': account, 'title': f'Do you really want to remove your {account.currency} account?'}
        return render(request, 'expense/delete.html', context)
    else:
        raise Http404


@login_required(login_url="/profile/login/")
def account_detail_divided(request, a_id):
    account = get_object_or_404(Account, pk=a_id)
    if request.user == account.user:
        incomes = Income.objects.filter(account=account)
        spendings = Spending.objects.filter(account=account)
        balance_trackers = BalanceTracker.objects.filter(account=account)

        # Chartit graph:
        def date_short(date):
            return date.strftime('%-d %b %Y %H:%M:%S')

        # Create a DataPool
        balance = DataPool(
            series=
            [{'options': {
                'source': BalanceTracker.objects.filter(account=account)},
                'terms': [{'date': 'date',
                           'amount': 'amount'}]
            },

            ])

        cht = Chart(
            datasource=balance,
            series_options=
            [{'options': {
                'type': 'line',
                'stacking': False},
                'terms': {
                    'date': [
                        'amount']
                }}],
            chart_options=
            {'title': {
                'text': 'Your balance over days'},
                'xAxis': {
                    'title': {'text': 'Dates'}},
                'yAxis': {
                    'title': {'text': f'Balance in {account.currency}'}},
                'legend': {
                    'layout': 'vertical',
                    'align': 'right',
                    'verticalAlign': 'center',
                    'x': -10,
                    'y': 80,
                    'floating': True,
                    'borderWidth': 1,
                    "backgroundColor": '#EEEEEE',
                    'shadow': True,
                    'reversed': True}}
        , x_sortf_mapf_mts=(None, date_short, False)
        )

        context = {'account': account, 'incomes': incomes, 'spendings': spendings, 'balance_trackers': balance_trackers,
                   'chart_list': [cht]}
        return render(request, 'expense/account-detail-divided.html', context)
    else:
        raise Http404


@login_required(login_url="/profile/login/")
def account_detail(request, a_id):
    account = get_object_or_404(Account, pk=a_id)
    if request.user == account.user:
        incomes = Income.objects.filter(account=account)
        spendings = Spending.objects.filter(account=account)
        balance_trackers = BalanceTracker.objects.filter(account=account)
        all_expenses = []
        for income in incomes:
            all_expenses.append(income)

        for spending in spendings:
            all_expenses.append(spending)

        def quick_sort(seq):
            length = len(seq)
            if length <= 1:
                return seq
            else:
                pivot = seq.pop()
            greater = []
            lower = []
            for expense in seq:
                if expense.date > pivot.date:
                    lower.append(expense)
                else:
                    greater.append(expense)
            return quick_sort(lower) + [pivot] + quick_sort(greater)

        everything = quick_sort(all_expenses)

        # Chartit graph:

        def date_short(date):
            return date.strftime('%-d %b %Y %H:%M:%S')

        # Create a DataPool
        balance = DataPool(
            series=
            [{'options': {
                'source': BalanceTracker.objects.filter(account=account)},
                'terms': [{'date': 'date',
                           'amount': 'amount'}]
            },

            ])

        cht = Chart(
            datasource=balance,
            series_options=
            [{'options': {
                'type': 'line',
                'stacking': False},
                'terms': {
                    'date': [
                        'amount']
                }}],
            chart_options=
            {'title': {
                'text': 'Your balance over days'},
                'xAxis': {
                    'title': {'text': 'Dates'}},
                'yAxis': {
                    'title': {'text': f'Balance in {account.currency}'}},
                'legend': {
                    'layout': 'vertical',
                    'align': 'right',
                    'verticalAlign': 'center',
                    'x': -10,
                    'y': 80,
                    'floating': True,
                    'borderWidth': 1,
                    "backgroundColor": '#EEEEEE',
                    'shadow': True,
                    'reversed': True}}
        , x_sortf_mapf_mts=(None, date_short, False)
        )

        context = {'account': account, 'incomes': incomes, 'spendings': spendings, 'balance_trackers': balance_trackers,
                   'everything': everything, 'chart_list': [cht]}
        return render(request, 'expense/account-detail.html', context)
    else:
        raise Http404


@login_required(login_url="/profile/login/")
def create_income(request, a_id):
    form = IncomeModelForm(request.POST or None)
    account = Account.objects.get(pk=a_id)
    context = {'form': form, 'title': 'Add a new income'}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.account = account
        account.current_balance += obj.amount
        obj.current_balance = account.current_balance
        account.save()
        obj.save()
        balance_tracker = BalanceTracker.objects.create(account=account, amount=account.current_balance, slug=obj.slug)
        return redirect(f'/account-detail/{a_id}/')
    return render(request, 'expense/form.html', context)


@login_required(login_url="/profile/login/")
def update_income(request, a_id, i_id):
    account = Account.objects.get(pk=a_id)
    income = get_object_or_404(Income, pk=i_id)
    balance_tracker = BalanceTracker.objects.get(account=account, slug=income.slug)
    all_newer_trackers = BalanceTracker.objects.filter(account=account, date__gte=income.date).exclude(account=account, slug=income.slug)
    if account.user == request.user:
        form = IncomeModelForm(request.POST or None, instance=income)
        old_income = income.amount

        context = {'form': form, 'account': account, 'income': income, 'title': 'Edit your income'}
        if form.is_valid():
            obj = form.save(commit=False)
            account.current_balance -= old_income
            balance_tracker.amount -= old_income
            income.current_balance -= old_income

            account.current_balance += obj.amount
            balance_tracker.amount += obj.amount
            income.current_balance += obj.amount

            for tracker in all_newer_trackers:
                try:
                    related_income = Income.objects.get(slug=tracker.slug)
                    related_income.current_balance -= old_income
                    tracker.amount -= old_income

                    related_income.current_balance += obj.amount
                    tracker.amount += obj.amount
                    related_income.save()
                    tracker.save()
                except ObjectDoesNotExist:
                    related_spending = Spending.objects.get(slug=tracker.slug)
                    related_spending.current_balance -= old_income
                    tracker.amount -= old_income

                    related_spending.current_balance += obj.amount
                    tracker.amount += obj.amount
                    related_spending.save()
                    tracker.save()

            obj.save()
            account.save()
            balance_tracker.save()
            income.save()
            return redirect(f'/account-detail/{a_id}/')
        return render(request, 'expense/form.html', context)
    else:
        raise Http404


@login_required(login_url="/profile/login/")
def delete_income(request, a_id, i_id):
    account = get_object_or_404(Account, pk=a_id)
    income = get_object_or_404(Income, pk=i_id)
    all_newer_trackers = BalanceTracker.objects.filter(account=account, date__gte=income.date).exclude(account=account,
                                                                                                       slug=income.slug)
    old_income = income.amount
    if account.user == request.user:
        if request.method == 'POST':
            balance_tracker = BalanceTracker.objects.get(account=account, slug=income.slug)
            account.current_balance -= income.amount
            account.save()
            income.delete()
            balance_tracker.delete()

            for tracker in all_newer_trackers:
                try:
                    print(tracker)
                    related_income = Income.objects.get(slug=tracker.slug)
                    related_income.current_balance -= old_income
                    tracker.amount -= old_income
                    related_income.save()
                    tracker.save()
                except ObjectDoesNotExist:
                    related_spending = Spending.objects.get(slug=tracker.slug)
                    related_spending.current_balance -= old_income
                    tracker.amount -= old_income
                    related_spending.save()
                    tracker.save()

            return redirect(f'/account-detail/{a_id}/')
        context = {'account': account, 'income': income, 'title': 'Do you want to remove this income?'}
        return render(request, 'expense/delete.html', context)
    else:
        raise Http404


@login_required(login_url="/profile/login/")
def create_spending(request, a_id):
    form = SpendingModelForm(request.POST or None)
    account = Account.objects.get(pk=a_id)
    context = {'form': form, 'title': 'Add a new spending'}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.account = account
        account.current_balance -= obj.amount
        obj.current_balance = account.current_balance
        account.save()
        obj.save()
        balance_tracker = BalanceTracker.objects.create(account=account, amount=account.current_balance, slug=obj.slug)
        return redirect(f'/account-detail/{a_id}/')
    return render(request, 'expense/form.html', context)


@login_required(login_url="/profile/login/")
def update_spending(request, a_id, s_id):
    account = Account.objects.get(pk=a_id)
    spending = get_object_or_404(Spending, pk=s_id)
    balance_tracker = BalanceTracker.objects.get(account=account, slug=spending.slug)
    all_newer_trackers = BalanceTracker.objects.filter(account=account, date__gte=spending.date).exclude(account=account,
                                                                                                         slug=spending.slug)
    if account.user == request.user:
        form = SpendingModelForm(request.POST or None, instance=spending)
        old_spending = spending.amount

        context = {'form': form, 'account': account, 'spending': spending, 'title': 'Edit your spending'}
        if form.is_valid():
            obj = form.save(commit=False)
            account.current_balance += old_spending
            balance_tracker.amount += old_spending
            spending.current_balance += old_spending

            account.current_balance -= obj.amount
            balance_tracker.amount -= obj.amount
            spending.current_balance -= obj.amount

            for tracker in all_newer_trackers:
                try:
                    related_spending = Spending.objects.get(slug=tracker.slug)
                    related_spending.current_balance += old_spending
                    tracker.amount += old_spending

                    related_spending.current_balance -= obj.amount
                    tracker.amount -= obj.amount
                    related_spending.save()
                    tracker.save()
                except ObjectDoesNotExist:
                    related_income = Income.objects.get(slug=tracker.slug)
                    related_income.current_balance += old_spending
                    tracker.amount += old_spending

                    related_income.current_balance -= obj.amount
                    tracker.amount -= obj.amount
                    related_income.save()
                    tracker.save()

            obj.save()
            account.save()
            balance_tracker.save()
            spending.save()
            return redirect(f'/account-detail/{a_id}/')
        return render(request, 'expense/form.html', context)
    else:
        raise Http404


@login_required(login_url="/profile/login/")
def delete_spending(request, a_id, s_id):
    account = get_object_or_404(Account, pk=a_id)
    spending = get_object_or_404(Spending, pk=s_id)
    all_newer_trackers = BalanceTracker.objects.filter(account=account, date__gte=spending.date).exclude(account=account,
                                                                                                         slug=spending.slug)
    old_spending = spending.amount
    if account.user == request.user:
        if request.method == 'POST':
            balance_tracker = BalanceTracker.objects.get(account=account, slug=spending.slug)
            account.current_balance += spending.amount
            account.save()
            spending.delete()
            balance_tracker.delete()

            for tracker in all_newer_trackers:
                try:
                    related_income = Income.objects.get(slug=tracker.slug)
                    related_income.current_balance += old_spending
                    tracker.amount += old_spending
                    related_income.save()
                    tracker.save()
                except ObjectDoesNotExist:
                    related_spending = Spending.objects.get(slug=tracker.slug)
                    related_spending.current_balance += old_spending
                    tracker.amount += old_spending
                    related_spending.save()
                    tracker.save()

            return redirect(f'/account-detail/{a_id}/')
        context = {'account': account, 'spending': spending, 'title': 'Do you want to remove this spending?'}
        return render(request, 'expense/delete.html', context)
    else:
        raise Http404
