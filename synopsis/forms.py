from django import newforms as forms
from django.conf import settings
from django.utils.translation import gettext as _
from datetime import datetime, timedelta
import urlparse
from gabaluu.form_choices import COMMENT_TYPES
from gabaluu.synopsis.models import Synopsis
from gabaluu.synopsis.models import Tag
from gabaluu.synopsis.models import Comment

class SynopsisForm(forms.Form):
    """
    
    The synopsis form.
      
    """
    title = forms.CharField(label=_('Title'), max_length=50, required=True, 
                            widget=forms.TextInput(attrs={"class": "form-text-variable"}))
    text = forms.CharField(label=_('Text'), required=True,
                           widget=forms.Textarea(attrs={"cols": "50", "rows": "80",
                                                        "maxlength": "1000"}))
    article_url = forms.CharField(label=_('Article Url'), max_length=500, required=True, 
                                  widget=forms.TextInput(attrs={"class": "form-text-variable"}))
    tags = forms.CharField(label=_('Tags'), max_length=100, required=False, 
                           widget=forms.TextInput(attrs={"class": "form-text-variable"}))
            
    def save(self, synopsis, author):
        data = self.data
        synopsis.title = data['title']
        synopsis.article_url = data['article_url']
        synopsis.text = data['text']
        synopsis.pub_date = datetime.now()
        synopsis.author = author
        synopsis.score = 0
        synopsis.permalink = Synopsis.create_permalink(title=data['title'], 
                                                      article_url=data['article_url'])
        url_parts = urlparse.urlparse(data['article_url'])
        protocol, domain = url_parts[:2]
        synopsis.article_site_url = '%s://%s' % (protocol, domain)
        
        synopsis.save()
        
        tag_list = Tag.parse(data['tags'])
        for tag_name in tag_list:
            tag = Tag.find_or_create(name=tag_name)
            tag.save()
            synopsis.tags.add(tag)
        
    def update(self, synopsis):
        data = self.data
        synopsis.text = data['text']
        synopsis.updated_date = datetime.now()
        synopsis.save()

        tag_list = Tag.parse(data['tags'])
        for tag_name in tag_list:
            tag = Tag.find_or_create(name=tag_name, new_synopsis=False)
            tag.save()
            synopsis.tags.add(tag)

class CommentForm(forms.Form):
   """

   The comment form.

   """

   def save(self, synopsis, comment_id, posted_by):
       #data = self.cleaned_data
       data = self.data
       text = data['comment']
       type_of = Comment.type_from_friendly_name('Feedback')
       comment = Comment.objects.create(posted_by=posted_by,
                                        text=text, 
                                        date=datetime.now(),
                                        type_of=type_of,
                                        synopsis=synopsis,
                                        reply_to=comment_id)
       return comment

class SearchForm(forms.Form):
   """

   The basic search form.

   """
   search_query = forms.CharField(label=_('Search'), max_length=200, required=True)

   def search(self):
       #data = self.cleaned_data
       data = self.data
       return Synopsis.query(data['search_query'])
