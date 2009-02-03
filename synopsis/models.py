from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import ObjectPaginator, InvalidPage
import re
import urlparse
from datetime import datetime, timedelta
from gabaluu.form_choices import COMMENT_TYPES

class Site(object):
    pass


class Tag(models.Model):
    name      = models.CharField(maxlength=100)
    count    = models.IntegerField()
    
    
    def _get_font_size(self):
        count = self.count + 10
        return "font-size: %spx;" % count
    font_size = property(_get_font_size)

    @classmethod
    def find_all(cls, site):
        return Tag.objects.all()

    @classmethod
    def find_or_create(cls, name, new_synopsis=True):      
        tag, created = Tag.objects.get_or_create(name=name, defaults={'count': 0 })
        
        if new_synopsis or (not new_synopsis and created):
            tag.count = tag.count + 1
         
        return tag

    @classmethod
    def find_by(cls, name):
        tags = Tag.objects.filter(name=str(name).strip())
        if tags.count() == 0:
            return None
        return tags[0]

    @classmethod
    def parse(cls, tags):
     """
        Parses a comma separated list of tags into 
        tag names handles all kinds of different tags. 
        (comma seperated, space seperated)
        Todo...Enhance to support more formats (in quotes)
     """
     return re.split('[,\\s]+', tags)



class Synopsis(models.Model):
     """
     A synopsis of a web resource.

     """
     title = models.CharField(maxlength=50)
     permalink = models.CharField(maxlength=100)
     text = models.CharField(maxlength=5000)
     article_site_url = models.CharField(maxlength=500)
     article_url = models.CharField(maxlength=500)
     pub_date = models.DateTimeField(editable=False)
     updated_date = models.DateTimeField(editable=False, blank=True, null=True)
     author = models.ForeignKey(User, related_name='author_id')
     tags = models.ManyToManyField(Tag)
     score = models.IntegerField()
     
     
     def __str__( self ):
         return self.title
     
     def get_absolute_url(self):
         return "http://zenopsis.com/synopsis/%s/" % self.permalink
     
     def is_author_of_synopsis(self, user):
         if self.author.username == user.username:
             return True
         return False
         
     @classmethod
     def create_permalink(cls, title, article_url):
         url_parts = urlparse.urlparse(article_url)
         title = Synopsis._remove_special_char(title)
         return "_".join((url_parts[1].replace('.', '_'), title))
         
     @classmethod   
     def _remove_special_char(cls, string):
         string = string.strip().replace(' ', '_')
         string = string.replace("'", "")
         string = string.replace("$", "")
         string = string.replace("&", "")
         string = string.replace("<", "")
         string = string.replace(">", "")
         string = string.replace("*", "")
         string = string.replace("@", "")
         string = string.replace(".", "")
         string = string.replace(":", "")
         string = string.replace("|", "")
         string = string.replace("~", "")
         string = string.replace("`", "")
         string = string.replace("(", "")
         string = string.replace(")", "")
         string = string.replace("%", "")
         string = string.replace("#", "")
         string = string.replace("^", "")
         string = string.replace("?", "")
         string = string.replace("/", "")
         string = string.replace("{", "")
         string = string.replace("}", "")
         string = string.replace(",", "")
         string = string.replace(";", "")
         string = string.replace("!", "")
         string = string.replace("+", "")
         string = string.replace("=", "")
         string = string.replace("-", "_")
         return string
 
     @classmethod
     def _run_query(cls, query, pagination=False, current_page=0, items_per_page=10):
         if pagination:
             paginator = ObjectPaginator(query, items_per_page)
             synopsis_list = paginator.get_page(current_page)
         else:
             paginator = None
             synopsis_list = query
         return synopsis_list, paginator
         
     @classmethod
     def most_recent(cls, pagination=False, current_page=0, items_per_page=10):
         return Synopsis._run_query(Synopsis.objects.all().order_by('-pub_date'), 
                                    pagination=pagination, 
                                    current_page=current_page, 
                                    items_per_page=items_per_page)
         
     @classmethod
     def popular(cls, pagination=False, current_page=0, items_per_page=10):
         return Synopsis._run_query(Synopsis.objects.all().order_by('-score', '-pub_date'), 
                                    pagination=pagination, 
                                    current_page=current_page, 
                                    items_per_page=items_per_page)
     @classmethod
     def by_tag(cls, tag, pagination=False, current_page=0, items_per_page=10):
         return Synopsis._run_query(Synopsis.objects.filter(tags__name__exact=tag).order_by('-pub_date'), 
                                   pagination=pagination, 
                                   current_page=current_page, 
                                   items_per_page=items_per_page)

     @classmethod
     def user_posted_synopsis_list(cls, user):
         return Synopsis.objects.filter(author=user).order_by('-pub_date')
     
     @classmethod
     def user_voted_synopsis_list(cls, user):
         election_list = Election.objects.filter(user=user).order_by('-date')
         return [election.synopsis for election in election_list]
    
     @classmethod
     def user_commented_synopsis_list(cls, user):
         comment_list = Comment.objects.filter(posted_by=user).order_by('-date')
         return [comment.synopsis for comment in comment_list] 
           
     @classmethod
     def query(cls, query):
         # todo -- improve search logic to search across all model fields
         return Synopsis.objects.filter(title__icontains=query)
           
     @classmethod
     def by_article_site(cls, site): 
         article_site_url = "http://%s" % site.replace('_', '.')     
         return Synopsis.objects.filter(article_site_url=article_site_url).order_by('-pub_date')

     
     def _published(self):
         """Return the synopsis formated published date."""
         return  self.pub_date.strftime('%B %d, %Y')
     published = property(_published)
 
     def _tags_as_string(self):
         tags_string = ""
         for tag in self.tags.all():
             tags_string =  ' '.join((tags_string, tag.name))

         return tags_string.strip()
     tags_as_string = property(_tags_as_string)
 
     def _short_text(self):
         text = "%s <a href='/synopsis/%s'>More >> </a>" % (self.text[:200], 
                                                             self.permalink)
         return text
     short_text = property(_short_text)
 
     def _short_text_preview(self):
         text = "<h2>%s</h2> %s <a href='/synopsis/%s' target='_top'>More >> </a>" % (self.title,
                                                                             self.text[:200], 
                                                                             self.permalink)
         return text
     short_text_preview = property(_short_text_preview)
     
     def _get_comments(self):
         """Return list of comments on this synopsis. """
         return Comment.objects.filter(synopsis=self, type_of="1", reply_to__isnull=True)
     comments = property(_get_comments)
     
     def _number_of_comments(self):
         count = len(Comment.objects.filter(synopsis=self, type_of="1"))
         if count == 1:
             return str(count) + " comment"
         else:
             return str(count) + " comments"
     number_of_comments = property(_number_of_comments)
 
     def _get_revisions(self):
         """Return list of revision comments on this synopsis. """
         return Comment.objects.filter(synopsis=self, type_of="2")
     revisions = property(_get_revisions)
 
     def _get_votes(self):
         count = self.score
         if count == 1:
             return str(count) + " vote"
         else:
             return str(count) + " votes"
     votes = property(_get_votes)
     
    
     @classmethod
     def article_site_list(cls):
         from django.db import connection
         cursor = connection.cursor()
         sql = """select article_site_url, count(article_site_url) from synopsis_synopsis 
                  group by article_site_url having count(article_site_url) >= 1 """
         cursor.execute(sql)
         rows = cursor.fetchall()
         site_list = []
         for row in rows:
             url_parts = urlparse.urlparse(row[0])
             site = Site()
             site.key = url_parts[1].replace('.', '_')
             site.url = url_parts[1]
             site.count = row[1]
             site_list.append(site)
         return site_list
         
     @classmethod
     def tag_and_article_site_list(cls):
         site_list = Synopsis.article_site_list()
         tag_list = Tag.objects.all()
         
         tags = []
         for t in tag_list:
            t.uri = "/tags/%s/" % t.name
            tags.append(t)
             
         for site in site_list:
             tag = Tag()
             tag.uri = "/sites/%s/" % site.key
             tag.name = site.key.replace('_', '.')
             tag.name = tag.name.replace('www.', '')
             tag.count = site.count
             tags.append(tag)
         
         return tags


              
class Election(models.Model):
     """
     Map if a user voted on a synopsis.

     """
     synopsis = models.ForeignKey(Synopsis)
     user = models.ForeignKey(User)
     date = models.DateTimeField(editable=False)
     
     @classmethod
     def has_voted(cls, user, synopsis):
         try:
             election = Election.objects.get(user__id=user.id, 
                                             synopsis__id=synopsis.id)
         except:
             return False
         
         return True
         
     @classmethod
     def vote(cls, synopsis, user):

         
         election = Election.objects.create(user=user,
                                            synopsis=synopsis,
                                            date=datetime.now())
                                        
         synopsis.score = synopsis.score + 1
         synopsis.save()
         
         return synopsis.votes
         


class Comment(models.Model):
     posted_by = models.ForeignKey(User, related_name='posted_by_id')
     text = models.CharField(maxlength=5000)
     date = models.DateTimeField(editable=False)
     type_of = models.CharField(maxlength=50)
     synopsis = models.ForeignKey(Synopsis)
     reply_to = models.IntegerField(blank=True, null=True)

     def _get_formated_dated(self):
         """Return formated date. """
         return self.date.strftime('%m/%d/%Y')
     formated_date = property(_get_formated_dated)
     
     def _get_comments(self):
         """Return list of comments on this comment. """
         return Comment.objects.filter(reply_to=self.id)
     comments = property(_get_comments)
     
     def _get_comment_type(self):
         """Return comment type. """
         comment_type = "None"
         for t in COMMENT_TYPES:
             if t[0] == int(self.type_of):
                 comment_type = t[1]
         return comment_type
     comment_type = property(_get_comment_type)
     
     
     def _short_text(self):
         text = "%s..<br/><a href='/synopsis/%s#comments-section'>More >></a>" % (self.text[:80], 
                                                             self.synopsis.permalink)
         return text
     short_text = property(_short_text)
     
     def is_revision(self):
         if self.type_of == "2":
             return True
             
     @classmethod
     def most_recent(cls):
        return Comment.objects.all().order_by('-date')[:8]
     
     @classmethod
     def type_from_friendly_name(cls, name):
         for t in COMMENT_TYPES:
              if t[1].lower() == name.lower():
                  return t[0]
         return "1"         



