from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from .forms import CreatePostForm
from .models import Post


class IndexView(generic.ListView):
    model = Post
    paginate_by = 20

    def get_queryset(self):
        return Post.objects.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["username"] = self.request.user.username

        return context


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
