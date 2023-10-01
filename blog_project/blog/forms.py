from django import forms
from blog.models import Post, Comments
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('author', 'title', 'text')
        # Fields that you should be able to edit while doin posts

        widgets = {
                'author': forms.TextInput(attrs={'class': 'textinputclass', 'value': '', 'id': 'username_field', 'type':'hidden'}),
                'title': forms.TextInput(attrs={'class': 'textinputclass'}),
                'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'})
        }

        """
        widgets sets class for css, allows to edit content via class we set here
        also 'editable medium-editor-textarea' is for javascript later
        """

class CommentsForm(forms.ModelForm):

    class Meta():
        model = Comments
        fields = ('author', 'text')
        # Fields that you should be able to edit while commenting

        widgets = {
            'author':forms.TextInput(attrs={'class': 'textinputclass'}),
            'text':forms.Textarea(attrs={'class': 'editable medium-editor-textarea textcontent postcontent'})
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']