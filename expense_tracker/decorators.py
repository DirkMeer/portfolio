from django.shortcuts import redirect
from django.contrib import messages

# Check if the user is NOT logged in. If logged in redirect to the home page.
def user_not_authenticated(function=None, redirect_url='/'):
# Immediately call decorator factory func | return it without calling if no func provided

    def decorator(view_func):
    # Decorates the _wrapped_view to be ran later, it is not called in the return

        def _wrapped_view(request, *args, **kwargs):
            # This is the function that replaces the decorated function
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        
        return _wrapped_view

    if function:
        return decorator(function) # pragma: no cover / decorator's functioning tested both ways
    
    return decorator


def redirect_demo_users_to_dash(function=None):
    # If user == demo user redirect to dash with message. Else just carry on.
    def decorator(view_func):

        def _wrapped_view(request, *args, **kwargs):
            if request.user.username[:9] == 'demo_user':
                messages.add_message(request, messages.ERROR, "Auto-generated demo accounts can not have their passwords changed or reset. Please make a real account if you want to try this functionality.")
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        
        return _wrapped_view
        
    if function:
        return decorator(function)
    
    return decorator