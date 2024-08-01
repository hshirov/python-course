from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from .forms import CreatePostForm, CommentForm
from .models import Post, Hashtag, Reaction
from .utils import get_dict_with_reactions_count

REACTION_TYPES = [c[0] for c in Reaction.REACTION_CHOICES]


class IndexView(generic.ListView):
    model = Post
    paginate_by = 20


class HashtagPostsView(generic.ListView):
    model = Post
    paginate_by = 20
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        hashtag = get_object_or_404(Hashtag, name=self.kwargs.get('hashtag').lower())
        return hashtag.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hashtag"] = self.kwargs.get('hashtag').lower()
        return context


class PostDetail(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        context['reaction_counts'] = get_dict_with_reactions_count(self.object, REACTION_TYPES)
        return context
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))


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

@login_required()
def react_to_post(request, pk, reaction):
    if reaction not in REACTION_TYPES:
        return HttpResponseBadRequest()
    
    post = get_object_or_404(Post, pk=pk)
    if post.reactions.filter(author=request.user, reaction_type=reaction).exists():
        return JsonResponse(get_dict_with_reactions_count(post, REACTION_TYPES))
    
    other_reactions = post.reactions.filter(author=request.user).exclude(reaction_type=reaction)
    if other_reactions.exists():
        other_reactions.delete()

    Reaction.objects.create(post=post, author=request.user, reaction_type=reaction)
    return JsonResponse(get_dict_with_reactions_count(post, REACTION_TYPES))
