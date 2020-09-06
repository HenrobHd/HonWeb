from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
import re
import sys

from . import util


def index(request):
    if request.method == "POST":
        exist = False
        if request.POST["title"] == "":
            return HttpResponse("You forget the title!")
        elif request.POST["edit"] == "edit":
            util.save_entry(request.POST["title"], request.POST["content"])
            util.save_entry_html(request.POST["title"], request.POST["content"])
            return HttpResponseRedirect(request.POST["title"])
        else:
            for title in util.list_entries():
                if request.POST["title"].upper() == title.upper():
                    exist = True

            if exist == False:
                util.save_entry(request.POST["title"], request.POST["content"])
                util.save_entry_html(request.POST["title"], request.POST["content"])
                return HttpResponseRedirect(request.POST["title"])
            else:
                return HttpResponse("This entry exists already!")
    else:
        randomPage = ""
        if len(util.list_entries()) == 0:
            randomPage = ""
            randomOnclick = "randoms(" + ");"
        else:
            randomPage = util.list_entries()[0]
            randomOnclick = ""

        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "randomPage": randomPage, "randomOnclick": randomOnclick
        })

#def randoms(request):
#   return HttpResponse("There are not any entries!")

def greet(request, name):
    if util.get_entry(name) != None:
        #link_patterns = [
            # Match a wiki page link LikeThis.
        #    (re.compile(r"(\b[A-Z][a-z]+[A-Z]\w+\b)"), r"/\1")
        #]
        #markdowner = Markdown(extras=["link-patterns"],
        #                       link_patterns=link_patterns)
        #con = util.get_entry(name)
        #content = markdowner.convert(con)

        if util.get_entry_html(name) == None:
                get = util.get_entry(name)
                util.save_entry_html(name, get)
        
        link = name + "/edit"
        delete = name + "/delete"
        return render(request, f"encyclopedia/{name}.html", {
            "title": name, "link": link, "delete": delete
        })
    else:
        return HttpResponse("This entry does not exists!")

def delete(request, title):
    if request.method == "POST":
        util.delete_entry(request.POST["ask"])
        util.delete_entry_html(request.POST["ask"])
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "encyclopedia/delete.html", {
            "filename": title
        })

listsclean = []
def search(request):
    listsclean = []
    exist = False
    for part in util.list_entries():
        if request.GET["q"].upper() == part.upper():
            link = part + "/edit"
            delete = part + "/delete"
            return render(request, f"encyclopedia/{part}.html", {
                "content": util.get_entry(part), "link": link, "delete": delete, "title": part
            })
        elif request.GET["q"].upper() in part.upper():
            exist = True
            listsclean.append(part)
    
    if exist == True:
        return render(request, "encyclopedia/search.html", {
            "lists": listsclean
        })
    else:
        return HttpResponse("This entry does not exists!")
        
def new(request):
    return render(request, "encyclopedia/new.html")

def edit(request, title):
    return render(request, "encyclopedia/edit.html", {
        "title": title, "content": util.get_entry(title)
    })