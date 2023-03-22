# Template tag to add classes to html tags
from django import template
register = template.Library()

@register.filter
def addclass(field, class_name):
    return field.as_widget(attrs={"class": class_name})