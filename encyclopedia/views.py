from django.shortcuts import render, redirect
from django.http import HttpResponse
from markdown2 import Markdown
from . import util
import random
import re

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if not entry:
        return HttpResponse('404 Error, Page Not Found!')
    markdowner = Markdown()
    text = markdowner.convert(entry)
    return render(request, "encyclopedia/entry.html", {"title": title, "text": text})

def search(request):
    if request.method == 'GET':
        q = request.GET.get('q','')
        entries = util.list_entries()
        if q in entries:
            return redirect('entry', title = q)
        matches = []
        for value in entries:
            if q in value:
                matches.append(value)
    return render(request, "encyclopedia/search.html", {"matches": matches})

def newpage(request):
    if request.method == "POST":
        title = request.POST.get('title','')
        content = request.POST.get('content','')
        if not title or not content:
            return HttpResponse('Submitted form was missing information!')
        if util.get_entry(title):
            return HttpResponse("Error: Page on Topic Already Exists")
        util.save_entry(title, content)
        return redirect('entry', title)
    return render(request, "encyclopedia/newpage.html")

def editpage(request, title):
    if request.method == "POST":
        content = request.POST.get('content','')
        if not content:
            return HttpResponse('Submitted empty form!')
        util.save_entry(title, content)
        return redirect('entry', title)
    entry = util.get_entry(title)
    return render(request, "encyclopedia/editpage.html", {"title":title, "entry":entry})


def randomly(request):
    entries = util.list_entries()
    magic_number = random.randint(0, len(util.list_entries()) - 1)
    title = entries[magic_number]
    return redirect(entry, title)
