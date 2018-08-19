from django import forms
from .models import Comment


# 定义评论的modelform
class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'content']

