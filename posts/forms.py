from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title","content","file","image","public"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
        widgets = {
            'comment': forms.TextInput(attrs={
                'class': 'form-control',
            })
        }