from django import forms
from .models import Post, Comment

class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)
    

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        # we use widgets in ModelForms like this:
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class PostSearchHome(forms.Form):
    search = forms.CharField()