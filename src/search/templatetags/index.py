from django import template
register = template.Library()

# Custom template tag for slicing in a template

@register.filter
def index(indexable, i):
    return indexable[i]