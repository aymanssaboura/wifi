from django import forms

from .models import Comment,Post,imagepath
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.forms import ModelForm, DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')



class Post(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('category', 'title','intro','body','status','image')
        
    
class Imagepath(forms.ModelForm):
    
    class Meta:
        model = imagepath
        fields = ('post','image',)