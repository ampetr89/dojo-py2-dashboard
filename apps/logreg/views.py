from django.shortcuts import render, redirect
from django.contrib import messages
from ..users.models import User 

def is_logged_in(request):
    return request.session.get('logged_in', False)

def index(request):
    if is_logged_in(request):
        return redirect('dash:home')
    else:
        return redirect('/login')

def login(request):
    if not is_logged_in(request):
        return render(request, 'logreg/login.html')
    else:
        return redirect('dash:home')

def register(request):
    if not is_logged_in(request):
        return render(request, 'logreg/register.html')
    else:
        return redirect('dash:home')

def process(request, form_type):
    
    if request.method=='GET':
        return redirect('logreg:login')

    
    if form_type == 'login':
        test_user = User(
            email = request.POST['email'].lower(),
            password_plaintext = request.POST['password']
        )
        test_user, errors = test_user.login_errors()

        for err_msg in errors:
            messages.error(request, err_msg)
        
        if len(errors) == 0:
            request.session['logged_in'] = True
            request.session['is_admin'] = test_user.is_admin
            request.session['first_name'] = test_user.first_name
            request.session['user_id'] = test_user.id
            
            return redirect('dash:home')
        else:
            return redirect('logreg:login')


    elif form_type in ['registration', 'create']:

        test_user = User(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'].lower(),
            password_plaintext = request.POST['password'],
            is_admin = bool(request.POST.get('is_admin', False))
        )

        test_user, errors = test_user.registration_errors()

        if request.POST['password'] != request.POST['password2']:
            errors.append("Passwords don't match")

        for err_msg in errors:
            messages.error(request, err_msg)
        
        if len(errors) == 0:
            test_user.encrypt_pw()
            test_user.save()
            if form_type=='registration':
                messages.success(request, "Registration successful! Please log in.")
                return redirect('logreg:login')
            else:
                messages.success(request, "User successfully created!")
                return redirect('dash:home') # or redirect('users:show', test_user.id)
        else:
            # errors in processing registration/ creation
            if form_type=='registration':
                return redirect('logreg:register')
            else:
                return redirect('users:new')

def logout(request):
    request.session.clear()
    return redirect('logreg:login')
