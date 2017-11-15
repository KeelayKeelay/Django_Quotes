# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from ..quoteapp.models import *

def index(request):
    context = {
        # 'messages':
    }
    return render(request, "login/index.html", context)

def register(request):
    if request.method == "POST":
        post_data = {
            'name':request.POST['name'],
            'alias':request.POST['alias'],
            'email':request.POST['email'],
            'password':request.POST['password'],
            'confirm_password':request.POST['confirm_password']
        }
        results = User.objects.register(post_data)
        if results['result'] == "failed_validation":
            if 'messages' in results.keys():
                for message in results['messages']:
                    messages.error(request, message)
            return redirect('login:index')
        else:
            if 'user' in results.keys():
                request.session['current_user'] = results['user'].id
                if 'messages' in results.keys():
                    for message in results['messages']:
                        messages.success(request, message)
                return redirect('login:index')
            return redirect('quoteapp:home')
        print results
    return redirect('login:index')


def login(request):
    if request.method == "POST":
        post_data = {
            'email':request.POST['email'],
            'password':request.POST['password']
        }
        login_result = User.objects.login(post_data)
        if login_result['result'] == "are_errors":
            if 'messages' in login_result.keys():
                for message in login_result['messages']:
                    messages.error(request, message)
            return redirect('login:index')
        else:
            if 'user' in login_result.keys():
                request.session['current_user'] = login_result['user'].id
            else:
                messages.error(request, "Something went wrong")
                return redirect('login:index')
            return redirect('quoteapp:home')

def logout(request):
    request.session.clear()
    messages.success(request, "Successfully logged out")
    return redirect('login:index')