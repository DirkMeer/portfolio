from django.shortcuts import redirect

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