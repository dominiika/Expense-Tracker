from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            # log me in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(
                username=username,
                password=password
            )
            login(request, user)
            return redirect('/')

    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'account/signup.html', context)
