from django import forms
from .models import ArticlePost

#create class of model
class ArticlePostForm(forms.ModelForm):
    class Meta:
        #clairfy reference of article
        model = ArticlePost
        # define the fields of words
        fields = ('title','body')
