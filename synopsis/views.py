from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.core.paginator import InvalidPage
from django.contrib.syndication.feeds import Feed
from gabaluu.synopsis.models import Synopsis
from gabaluu.synopsis.models import Election
from gabaluu.synopsis.models import Tag
from gabaluu.synopsis.models import Comment
from gabaluu.synopsis.forms import SynopsisForm
from gabaluu.synopsis.forms import CommentForm
from gabaluu.synopsis.forms import SearchForm
import captcha


class Page(object):
    pass
    
class PopularFeed(Feed):
    title = "Zenopsis.com popular"
    link = "/popular/"
    description = "Most popular synopsis items."
    
    def items(self):
        return Synopsis.objects.all().order_by('-score', '-pub_date')[:5]

class RecentFeed(Feed):
    title = "Zenopsis.com most recent"
    link = "/recent/"
    description = "Most recent synopsis items."

    def items(self):
        return Synopsis.objects.all().order_by('-pub_date')[:5]



def index(request):
    return HttpResponseRedirect("/popular/")

def recent(request, current_page=0, template_name='recent.html'):
    """
    Recent list page.
    
    Context::
        None
    
    Template::
        recent.html
    
    """
    has_next_page = False
    has_previous_page = False
    pages = []
    
    try:
        synopsis_list, p = Synopsis.most_recent(pagination=True, 
                                                current_page=int(current_page), 
                                                items_per_page=5)
    except InvalidPage:
        #todo..redirect to 404 not found page...
        return HttpResponseRedirect("/")
        
    if p:
        has_next_page = p.has_next_page(int(current_page))
        has_previous_page = p.has_previous_page(int(current_page))
        for pn in range(p.pages):
            if pn != 0:
                page = Page()
                page.number = pn
                if pn == int(current_page):
                    page.is_current = True
                pages.append(page)
        
    #tag_list = Tag.objects.all()
    tag_list = Synopsis.tag_and_article_site_list()
    article_site_list = Synopsis.article_site_list()

    
    return render_to_response(template_name, 
                            dict(synopsis_list=synopsis_list,
                                 tag_list=tag_list,
                                 article_site_list=article_site_list,
                                 has_next_page=has_next_page,
                                 has_previous_page=has_previous_page,
                                 current_page=int(current_page),
                                 pages=pages,
                                 recent_comment_list=Comment.most_recent()),
                            context_instance=RequestContext(request))


def popular(request, current_page=0, template_name='popular.html'):
    """
    Most popular synopsis list.

    Context::
        None

    Template::
        popular.html

    """
    has_next_page = False
    has_previous_page = False
    pages = []
    
    try:
        synopsis_list, p = Synopsis.popular(pagination=True, 
                                         current_page=int(current_page), 
                                         items_per_page=5)
    except InvalidPage:
        #todo..redirect to 404 not found page...
        return HttpResponseRedirect("/")
        
    if p:
        has_next_page = p.has_next_page(int(current_page))
        has_previous_page = p.has_previous_page(int(current_page))
        for pn in range(p.pages):
            if pn != 0:
                page = Page()
                page.number = pn
                if pn == int(current_page):
                    page.is_current = True
                pages.append(page)
        
    #tag_list = Tag.objects.all()
    tag_list = Synopsis.tag_and_article_site_list()
    article_site_list = Synopsis.article_site_list()

    return render_to_response(template_name, 
                            dict(synopsis_list=synopsis_list,
                                 tag_list=tag_list,
                                 article_site_list=article_site_list,
                                 has_next_page=has_next_page,
                                 has_previous_page=has_previous_page,
                                 current_page=int(current_page),
                                 pages=pages,
                                 recent_comment_list=Comment.most_recent()),
                            context_instance=RequestContext(request))


def tagged(request, tag, current_page=0, template_name='tagged.html'):
    """
    Tagged synopsis list.

    Context::
        None

    Template::
        tagged.html

    """
    has_next_page = False
    has_previous_page = False
    pages = []
    
    try:
        synopsis_list, p = Synopsis.by_tag(tag=tag, 
                                         pagination=True, 
                                         current_page=int(current_page), 
                                         items_per_page=5)
    except InvalidPage:
        #todo..redirect to 404 not found page...
        return HttpResponseRedirect("/")
        
    if p:
        has_next_page = p.has_next_page(int(current_page))
        has_previous_page = p.has_previous_page(int(current_page))
        for pn in range(p.pages):
            if pn != 0:
                page = Page()
                page.number = pn
                if pn == int(current_page):
                    page.is_current = True
                pages.append(page)
    
    base_path = "tags/%s" % tag
    #tag_list = Tag.objects.all()
    tag_list = Synopsis.tag_and_article_site_list()
    article_site_list = Synopsis.article_site_list()

    return render_to_response(template_name, 
                            dict(synopsis_list=synopsis_list,
                                 tagged=tag,
                                 tag_list=tag_list,
                                 article_site_list=article_site_list,
                                 has_next_page=has_next_page,
                                 has_previous_page=has_previous_page,
                                 current_page=int(current_page),
                                 pages=pages,
                                 base_path=base_path,
                                 recent_comment_list=Comment.most_recent()),
                            context_instance=RequestContext(request))


def sites(request, site, template_name='sites.html'):
    """
    Site synopsis list.

    Context::
        None

    Template::
        tagged.html

    """
    synopsis_list = Synopsis.by_article_site(site=site)
    #tag_list = Tag.objects.all()
    tag_list = Synopsis.tag_and_article_site_list()
    article_site_list = Synopsis.article_site_list()

    return render_to_response(template_name, 
                            dict(synopsis_list=synopsis_list,
                                 site=site,
                                 tag_list=tag_list,
                                 article_site_list=article_site_list,
                                 recent_comment_list=Comment.most_recent()),
                            context_instance=RequestContext(request))


def terms(request, template_name='terms.html'):
    """
    Terms of Service.

    Context::
        None

    Template::
        terms.html

    """

    return render_to_response(template_name, 
                            context_instance=RequestContext(request))

def privacy(request, template_name='privacy.html'):
    """
    Privacy Policy
    
    Context::
        None

    Template::
        privacy.html

    """

    return render_to_response(template_name, 
                            context_instance=RequestContext(request))


def about(request, template_name='about.html'):
    """
    About the site

    Context::
        None

    Template::
        about.html

    """

    return render_to_response(template_name, 
                            context_instance=RequestContext(request))



@login_required
def synopsis_new(request, template_name='synopsis/synopsis_new.html'):
    """
     New Synopsis.

    Context::
        Synopsis

    Template::
       synopsis/synopsis_new.html

    """
    author = request.user
    captcha_form = captcha.displayhtml("6LfitQAAAAAAAPuPkbRUUbT6mjhFbTGaS_nwKjkl")
    
    if request.method == 'POST':
        
        recaptcha_challenge_field = request.POST["recaptcha_challenge_field"]
        recaptcha_response_field = request.POST["recaptcha_response_field"]
        private_key = "6LfitQAAAAAAAGlpZA4DyouLEWRkfqLwBawQAxrq"
        remoteip = request.META['REMOTE_ADDR']
        
        captcha_response = captcha.submit(recaptcha_challenge_field=recaptcha_challenge_field,
                                          recaptcha_response_field=recaptcha_response_field,
                                          private_key=private_key,
                                          remoteip=remoteip)
                                          
        
        if captcha_response.is_valid:                                  
        
            form = SynopsisForm(request.POST)
            if form.is_valid():
                form.save(synopsis=Synopsis(), author=author)
                return HttpResponseRedirect("/")
                
        else:
            form = SynopsisForm(request.POST)
            captcha_error = "<span style='color:red'>Incorrect captcha, please try again!</span>"

    else:
        form = SynopsisForm()
        captcha_error = ""


    return render_to_response(template_name, 
                            dict(form=form, 
                                 captcha_form=captcha_form,
                                 captcha_error=captcha_error),
                            context_instance=RequestContext(request))


@login_required
def synopsis_edit(request, permalink, template_name='synopsis/synopsis_edit.html'):
    """
     Edit Synopsis.

    Context::
        Synopsis

    Template::
       synopsis/synopsis_edit.html

    """
    
    synopsis = Synopsis.objects.get(permalink=permalink)
    
    if not synopsis:
        #todo..redirect to 404 not found page...
        return HttpResponseRedirect("/")
    
    if not synopsis.is_author_of_synopsis(user=request.user):
        return HttpResponseRedirect("/")
        
    
    
    if request.method == 'POST':
        form = SynopsisForm(request.POST)
        form.update(synopsis=synopsis)
        return HttpResponseRedirect("/synopsis/%s" % synopsis.permalink)

    else:
        form = SynopsisForm(synopsis.__dict__)
 

    return render_to_response(template_name, 
                            dict(form=form, synopsis=synopsis),
                            context_instance=RequestContext(request))
                            

def synopsis_detail(request, permalink, template_name='synopsis/synopsis_detail.html'):
    """
     Detail of a Synopsis.

    Context::
        Synopsis

    Template::
       synopsis/synopsis_detail.html

    """
    synopsis = Synopsis.objects.get(permalink=permalink)
    
    
    return render_to_response(template_name, 
                            dict(synopsis=synopsis,
                                 comment_form=CommentForm(),
                                 tag_list=Synopsis.tag_and_article_site_list(),
                                 article_site_list=Synopsis.article_site_list(),
                                 recent_comment_list=Comment.most_recent()),
                            context_instance=RequestContext(request))


def synopsis_preview(request, permalink, template_name='synopsis/synopsis_preview.html'):
    """

    """

    synopsis = Synopsis.objects.get(permalink=permalink)

    return render_to_response(template_name,
                              dict(synopsis=synopsis),
                                   context_instance=RequestContext(request))

    
def synopsis_link(request, synopsis_id, template_name='synopsis/synopsis_link.html'):
    """
    Link to a synopsis from another site.

    Context::
        Synopsis

    Template::
       synopsis/synopsis_link.html

    """

    synopsis = Synopsis.objects.get(id=synopsis_id)

    return render_to_response(template_name, 
                            dict(synopsis=synopsis),
                            context_instance=RequestContext(request))
                            
                            
@login_required
def comment_create(request, synopsis_id, comment_id=None, template_name='synopsis/comment.html'):
    """
     Create a comment.  Invoked by AJAX call.

    Context::
        Comment

    Template::
       synopsis/comment.html

    """
    if request.method == 'POST':
        synopsis = Synopsis.objects.get(id=synopsis_id)
        

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(synopsis=synopsis, 
                                posted_by=request.user,
                                comment_id=comment_id)
    else:
        return HttpResponseRedirect("/")

    return render_to_response(template_name, dict(comment=comment),                        
                              context_instance=RequestContext(request))



def synopsis_vote(request, synopsis_id):
    """
     Vote for a synopsis.  Invoked by AJAX call.

    Context::
        synopsis_id

    Template::
       none

    """
    
    synopsis = Synopsis.objects.get(id=synopsis_id)
    
    has_voted = Election.has_voted(user=request.user, synopsis=synopsis)
    
    if has_voted:
        votes = synopsis.votes
    else:
        votes = Election.vote(synopsis=synopsis, user=request.user)
    
    
    json_response = """{'synopsis': '%s',
                        'votes': '%s' }""" % (synopsis_id, str(votes))


    return HttpResponse(json_response)
    
    
def synopsis_search(request, template_name='search.html'):
    """
    Search page for the site.

    Context::
        None

    Template::
        search.html

    """

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            synopsis_list = form.search()

    else:
        form = SearchForm()
        synopsis_list = []
    return render_to_response(template_name,
                              dict(form=form, synopsis_list=synopsis_list),
                                   context_instance=RequestContext(request))


