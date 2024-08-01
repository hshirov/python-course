from django import forms
from .models import Post, Comment


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text_content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title'}),
            'text_content': forms.Textarea(attrs={'placeholder': 'Whats on your mind...'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text_content']
        widgets = {'text_content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add a comment...'})}
        labels = {'text_content': ''}
