from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def get_stream(indexable, stream):
    print("Templatetag_getstream",indexable, stream)
    return "okis"
    #return indexable[stream]