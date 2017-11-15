from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *

def home(request):
    user = User.objects.get(pk=request.session['current_user'])
    context = {
        # "messages": Quote.objects.messenger()[0],
        "quotes":Quote.objects.exclude(users__id = user.id)
    }
    if "current_user" in request.session.keys():
        context['user'] = user
    return render(request, "quoteapp/home.html", context)

def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    context = {
        "user":user,
        "posts":Quote.objects.filter(user=user)
    }
    context['num_posts'] = len(context['posts'])
    return render(request, "quoteapp/profile.html", context)

def process_quote(request):
    if request.method == "POST":
        no_errors = True
        quoted_user = request.POST['quoted_user']
        if len(quoted_user) < 3:
            no_errors = False
            messages.error(request, "Quoted By field requires at least 3 characters")
        content = request.POST['content']
        if len(content) < 10:
            no_errors = False
            messages.error(request, "Message requires at least 10 characters")
        if no_errors:
            user = User.objects.get(pk=request.session['current_user'])
            Quote.objects.create(quoted_user=quoted_user, content=content, user=User.objects.get(pk=int(user.id)))
    return redirect('quoteapp:home')


def favadd(request, quote_id):
    user = User.objects.get(pk=request.session['current_user'])
    quote = Quote.objects.get(pk=quote_id)
    user.quotes.add(quote)
    return redirect('quoteapp:home')

def favrem(request, quote_id):
    user = User.objects.get(pk=request.session['current_user'])
    quote = Quote.objects.get(pk=quote_id)
    user.quotes.remove(quote)
    return redirect('quoteapp:home')