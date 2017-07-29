from django.shortcuts import render, redirect
from ..users.models import User 

def is_logged_in(request):
    return request.session.get('logged_in', False)

def is_admin(request):
    return request.session.get('is_admin', False)

def index(request):
    if is_logged_in(request):
        
        context = {
            'users': User.objects.all(),
            'is_admin': is_admin(request)
        }
        return render(request, 'dash/index.html', context)
        """
        if not context['is_admin']:
            
            return render(request, 'dash/index.html', context)
        else:
            return redirect('dash:admin', context)
        """
    else:
        return redirect('logreg:login')
    
"""
def admin(request):
    if is_admin(request):
        context = {
                'users': User.objects.all(),
                'is_admin': True
            }
        return render(request, 'dash/index.html', context)
    else:
        return redirect('dash:index')
"""