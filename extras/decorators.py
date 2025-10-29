# Em extras/decorators.py

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def group_required(*group_names):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "Você não tem permissão para acessar esta página.")
                return redirect('list_activities')
        return _wrapped_view
    return decorator