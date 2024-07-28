from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .forms import SignUpForm, AuthForm
from .decorators import anonymous_required


@anonymous_required
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'userauth/signup.html', {'form': form})

@anonymous_required
def login(request):
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthForm()
    return render(request, 'userauth/login.html', {'form': form})
