from django.forms import ModelForm

from .models import Post

from django import forms
from django.forms import FileInput, TextInput



class PostForm(ModelForm):
    error_css_class = "error-field"
    required_css_class = "required-field"

    cover = forms.FileField(widget = forms.FileInput(attrs = {'class' : 'create-cover'}))
    description = forms.CharField(widget = forms.Textarea(attrs = {'class' : 'create-description', 'placeholder' : 'enter description...'}))

    class Meta:
        model = Post
        fields = ['cover', 'description']
        exclude = ['owner', 'likes']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""


    
