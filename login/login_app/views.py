from django.shortcuts import render, redirect
from .models import User
import bcrypt
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashedpassword = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(request.POST['password'])
        print(hashedpassword)
        new_user = User.objects.create(
            fname = request.POST['fname'],
            lname = request.POST['lname'],
            email = request.POST['email'],
            password = hashedpassword
        )
        request.session['user_id'] = new_user.id
        return redirect('/success')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user = User.objects.get(email=request.POST['logemail'])
            request.session['user_id'] = user.id
            return redirect('/success')
    else:
        return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        "user": user
    }
    return render(request, 'success.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')