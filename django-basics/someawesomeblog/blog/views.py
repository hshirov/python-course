from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import generic
from .forms import CreatePostForm
from .models import Post, Hashtag


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
    

class HashtagPostsView(generic.ListView):
    model = Post
    paginate_by = 20
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        hashtag = get_object_or_404(Hashtag, name=self.kwargs.get('hashtag').lower())
        return Post.objects.filter(hashtags=hashtag).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hashtag"] = self.kwargs.get('hashtag').lower()
        return context


class PostDetail(generic.DetailView):
    model = Post


@login_required(login_url='/auth/login/')
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if (form.is_valid()):
            post = form.save(commit=False)
            post.author = request.user
            form.save()

            return redirect('home')
    else:
        form = CreatePostForm()

    return render(request, 'blog/create.html', {'form': form})
