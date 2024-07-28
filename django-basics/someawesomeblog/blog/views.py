from django.shortcuts import render

def home(request):
    context = {'username': None}
    if request.user.is_authenticated:
        context['username'] = request.user.username

    return render(request, 'blog/index.html', context)
