import re
from django import forms
from .models import Post, Hashtag, Comment

def extract_hashtags(text):
    """Extracts all hashtags from a string and returns them in a list."""
    hashtags = re.findall(r'#(\w+)', text)
    return hashtags


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text_content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title'}),
            'text_content': forms.Textarea(attrs={'placeholder': 'Whats on your mind...'}),
        }

    def save(self, commit=True):
        post = super().save(commit=False)
        hashtags = extract_hashtags(self.cleaned_data['text_content'])

        if commit:
            print('Commit')
            post.save()
            post.hashtags.clear()
            for tag in hashtags:
                tag_name = tag.strip().lower()
                if tag_name:
                    hashtag, created = Hashtag.objects.get_or_create(name=tag_name)
                    post.hashtags.add(hashtag)
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text_content']
        widgets = {'text_content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add a comment...'})}
        labels = {'text_content': ''}
