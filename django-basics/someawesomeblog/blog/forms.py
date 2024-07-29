from django import forms
from .models import Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text_content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title'}),
            'text_content': forms.Textarea(attrs={'placeholder': 'Whats on your mind...'}),
        }
