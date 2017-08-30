from django.shortcuts import render, redirect
from models import *
from django.contrib import messages

def index(request):
    return render(request, 'log_reg/index.html')

def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')

    context = {
            'user' : User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'log_reg/success.html', context)

def register(request):
    result = User.objects.reg_validate(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)        
        return redirect('/')
    else:
        request.session['user_id'] = result.id 
        messages.success(request, "You have successfuly registered!")
        return redirect('/success')

def login(request):
    result = User.objects.log_validate(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)        
        return redirect('/')
    else:
        request.session['user_id'] = result.id 
        messages.success(request, "You have successfuly logged in!")
        return redirect('/success')