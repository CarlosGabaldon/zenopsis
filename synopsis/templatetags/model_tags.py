from django.template import Library
from django.template import RequestContext
from gabaluu.synopsis.models import Election
from gabaluu.synopsis.models import Synopsis

# Setup register function for inclusion tags
register = Library()

@register.inclusion_tag('questions/comment.html')
def render_comment(comment):
    """
     Inclusion tag for rendering a comment.
    
    Context::
        Comment
    
    Template::
        questions/comment.html
    
    """
    return dict(comment=comment)
    
    
@register.inclusion_tag('synopsis/synopsis_list.html')
def render_synopsis_list(synopsis_list, user, 
                         has_previous_page=False, 
                         has_next_page=False,
                         current_page=None,
                         base_path="popular",
                         pages=None):
    """
     Inclusion tag for rendering a synopsis list.

    Context::
        Synopsis List

    Template::
        synopsis_list.html

    """
    
    previous_page = None
    next_page = None
    previous_page_is_first_page = False
    
    
    if current_page != None:
        if current_page == 1:
            previous_page_is_first_page = True
            
        else:
            previous_page = current_page - 1
        next_page = current_page + 1
        
    
    return dict(synopsis_list=synopsis_list, user=user, 
                has_previous_page=has_previous_page, 
                has_next_page=has_next_page,
                previous_page=previous_page,
                next_page=next_page,
                base_path=base_path,
                previous_page_is_first_page=previous_page_is_first_page,
                pages=pages)


@register.inclusion_tag('synopsis/synopsis.html')
def render_synopsis(synopsis, user, detail=False):
    """
     Inclusion tag for rendering a synopsis.

    Context::
        Synopsis

    Template::
        synopsis.html

    """
    has_voted = ""
    is_author_of_synopsis = False
    
    if user.is_authenticated():    
        if Election.has_voted(user=user, synopsis=synopsis):
            has_voted = "style='display: none;'"
            
        is_author_of_synopsis = synopsis.is_author_of_synopsis(user=user)
        
    else:
        has_voted = "style='display: none;'"
              
    tag_list = synopsis.tags.all()
    for t in tag_list:
        t.uri = "/tags/%s" % t.name
    
    return dict(synopsis=synopsis, detail=detail, has_voted=has_voted,
                is_author_of_synopsis=is_author_of_synopsis, tag_list=tag_list)

@register.inclusion_tag('synopsis/synopsis_article_site_list.html')
def render_synopsis_article_site_list(article_site_list):
    """
     Inclusion tag for rendering a list of web sites.

    Context::
        article_site_list

    Template::
        synopsis/synopsis_article_site_list.html

    """

    return dict(article_site_list=article_site_list)



@register.inclusion_tag('synopsis/tag_list.html')
def render_tag_list(tag_list):
    """
     Inclusion tag for rendering a tag list.

    Context::
        Tag List

    Template::
        tag_list.html

    """

    return dict(tag_list=tag_list)


@register.inclusion_tag('synopsis/comment_list.html')
def render_comment_list(comment_list, user, comment_list_css="main-thread"):
    """
     Inclusion tag for rendering a comment list.

    Context::
        Comment List

    Template::
        comment_list.html

    """
 
    return dict(comment_list=comment_list, comment_list_css=comment_list_css, user=user)

@register.inclusion_tag('synopsis/comment_list_recent.html')
def render_comment_list_recent(comment_list, user):
    """
     Inclusion tag for rendering a recent comment list.

    Context::
        Comment List

    Template::
        comment_list_recent.html

    """

    return dict(comment_list=comment_list, user=user)

@register.inclusion_tag('synopsis/comment.html')
def render_comment(comment, user=None):
    """
     Inclusion tag for rendering a comment.

    Context::
        Comment

    Template::
        comment.html

    """

    return dict(comment=comment, user=user)


@register.inclusion_tag('synopsis/comment_form.html')
def render_comment_form(synopsis, comment=None):
    """
     Inclusion tag for rendering a comment form.

    Context::
        Comment form

    Template::
        synopsis/comment_form.html

    """
    if comment:
        url = "/synopsis/%s/comments/%s/create/" % (synopsis.id, comment.id)
    else:
        url =  "/synopsis/%s/comments/create/" % (synopsis.id)

    return dict(synopsis=synopsis, url=url)



@register.inclusion_tag('accounts/profile_list.html')
def render_profile_list(profile_list):
    """
     Inclusion tag for rendering a list of profiles.

    Context::
        Profile List

    Template::
        accounts/profile_list.html

    """
    return dict(profile_list=profile_list)

@register.inclusion_tag('synopsis/textile_help.html')
def render_textile_help():
    """
     Inclusion tag for textile help.

    Context::
        

    Template::
        synopsis/textile_help.html

    """
    return {}

@register.inclusion_tag('terms_text.html')
def render_terms_text():
    """
     Inclusion tag for terms of service.

    Context::


    Template::
        terms_text.html

    """
    return {}

