from django import forms
from blog.models import Post, Comments


class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('author', 'title', 'text')
        # Fields that you should be able to edit while doin posts

        widgets = {
                'title':forms.TextInput(attrs={'class':'textinputclass'}),
                'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
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
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea textcontent'})
        }


