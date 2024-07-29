from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreatePostForm

def home(request):
    context = {'username': None}
    if request.user.is_authenticated:
        context['username'] = request.user.username

    return render(request, 'blog/index.html', context)

@login_required(login_url='/auth/login/')
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if (form.is_valid()):
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('home')
    else:
        form = CreatePostForm()

    return render(request, 'blog/create.html', {'form': form})
