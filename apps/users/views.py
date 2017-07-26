from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .models import Message

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
    return render(request, 'users/show.html', {'user': user})

def edit(request, user_id=None):
    if user_id:
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
        'is_admin': is_admin(request),
        'profile': profile
        }
    return render(request, 'users/edit.html', context)

def update(request, user_id, ud_type):
    user = User.objects.filter(id=user_id)
    if len(user) == 0:
        return redirect('dash:home')
    user = user[0]
    if ud_type=='info':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        # user.email = request.POST['email']
        if is_admin(request):
            user.is_admin = request.POST.get('is_admin', False)
            print('is admin:')
            print(user.is_admin)
        user, errors = user.registration_errors(exists_override=True, pw_override=True)
        if len(errors) == 0:
            user.save()
            messages.success(request, 'User info updated.')
        else:
            for err_msg in errors:
                messages.error(request, err_msg)
        return redirect('users:edit', user_id)

    elif ud_type=='password':
        user.password_plaintext = request.POST['password']
        user, errors = user.registration_errors(exists_override=True)
        if request.POST['password'] != request.POST['password2']:
            errors.append('Passwords do not match')

        if len(errors) == 0:
            user.encrypt_pw()
            user.save()
            messages.success(request, 'User password has been updated.')
        else:
            for err_msg in errors:
                messages.error(request, err_msg)
        return redirect('users:edit', user_id)

    elif ud_type=='description':
        user.description = request.POST['description']
        user.save()
        messages.success(request, 'User description has been updated.')
        return redirect('users:edit', user_id)

def delete(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('dash:home')

def new(request):
    return render(request, 'users/new.html')

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