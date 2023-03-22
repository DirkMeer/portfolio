import urllib
from django.shortcuts import redirect
from .models import Setting


# Reusable shortcut to add queries to our redirects
def query_redirect(url, params=None):
    response = redirect(url)
    if params:
        query_string = urllib.parse.urlencode(params)
        response['Location'] += '?' + query_string
    return response

# Get last visited dashboard year/month, so cancel button always redirects back correctly
def get_reference_year_month(request):
    last_visited_dash = Setting.objects.get(user=request.user.id)
    last_visited_month = last_visited_dash.last_viewed_year_month[4:]
    last_visited_year = last_visited_dash.last_viewed_year_month[:4] 
    return [last_visited_year, last_visited_month]

# Get the correct 1month forward and 1month backward dates (year and month)
def get_next_and_previous_month_and_year(month, year):
    context = {}
    if month == 1:
        context['month_minus'], context['year_minus'] = 12, year-1
    else:
        context['month_minus'], context['year_minus'] = month-1, year
    if month == 12:
        context['month_plus'], context['year_plus'] = 1, year+1
    else:
        context['month_plus'], context['year_plus'] = month+1, year
    return context