from django import template

register = template.Library()

def allow_bold_markup(text):
    return text.replace('**', '<strong>', 1).replace('**', '</strong>', 1)

register.filter('allow_bold_markup', allow_bold_markup)