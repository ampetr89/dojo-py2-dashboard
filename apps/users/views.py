from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .models import Message
import logging

from dashboard.settings import SERVER_LOG


"""

logger = logging.getLogger('server')
logger.debug("Logging started for %s" % (SERVER_LOG))
hdlr = logging.FileHandler(SERVER_LOG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
"""

def is_logged_in(request):
    return request.session.get('logged_id', False)

def is_admin(request):
    return request.session.get('is_admin', False)

def index(request):
    if is_logged_in(request):
        return redirect('dash:home')
    else:
        return redirect('logreg:login')

def show(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'users/show.html', {'user': user, 'is_admin': is_admin(request)})

def edit(request, user_id=None):
    print(SERVER_LOG)
    SERVER_LOG.debug('we find ourselves in the edit function')
    if request.method == 'GET':
        # show the edit page if it's a GET request
        if user_id:
            if not is_admin(request):
                return redirect('dash:home')
            
            user = User.objects.filter(id=user_id)
            if len(user) == 0:
                return redirect('dash:home')
            else:
                user = user[0]
        else:
            user = User.objects.get(id=request.session['user_id'])

        profile = user.id == request.session['user_id']
        context = {
            'user': user, 
            'is_admin': is_admin(request), # if theyre an admin, can change other's info
            'profile': profile # if theyre editing their own profile, then they can edit the description
            }
        return render(request, 'users/edit.html', context)

    elif request.method == 'POST':
        # posting to this route handles editing the user
        SERVER_LOG.debug('we got data!')
        SERVER_LOG.debug(request.POST)
        user = User.objects.filter(id=user_id)
        if len(user) == 0:
            return redirect('dash:home')
        user = user[0]
        
        if 'password' in request.POST:
            # editing password
            user.password_plaintext = request.POST['password']
            user, errors = user.edit_pw()

            if request.POST['password'] != request.POST['password2']:
                errors.append('Passwords do not match')

            if len(errors) == 0:
                user.encrypt_pw()
                user.save()
                messages.success(request, 'User password has been updated.')
        else:
            # editing non-password fields
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.is_admin = bool(int(request.POST.get('is_admin', user.is_admin)))
            user.description = request.POST.get('description', user.description)
        
            user, errors = user.edit_info()        

            if len(errors) == 0:
                user.save()
                request.session['is_admin'] = user.is_admin
                
                
                messages.success(request, 'User info updated.')
        
        if len(errors) > 0:
            for err_msg in errors:
                messages.error(request, err_msg, extra_tags='danger')
        return redirect('users:edit', user_id)


def delete(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('dash:home')

def new(request):
    return render(request, 'users/new.html', {'is_admin': is_admin(request)})

def add_message(request, to_user_id):
    if request.method=='GET':
        return redirect('dash:home')

    from_user_id = request.session['user_id']
    
    content = request.POST['content']
    if len(content) > 0:
        new_message= Message.objects.create(
            from_user = User.objects.get(id=from_user_id),
            to_user = User.objects.get(id=to_user_id),
            content = content
        )
    return redirect('users:show', to_user_id)