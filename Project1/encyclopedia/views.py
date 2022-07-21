from tkinter import Entry
from django.shortcuts import redirect, render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util

import markdown2


def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {"entries": entries})


def title(request, title):
    entries = util.list_entries()
    up_entries = [entry.upper() for entry in entries]
    if title.upper() in up_entries:
        content = markdown2.markdown(util.get_entry(title))
        return render(
            request,
            "encyclopedia/titles.html",
            {"content": content, "title": title},
        )
    else:
        return render(
            request,
            "encyclopedia/error.html",
            {"error": "The requested page was not found."},
        )


def search(request):
    entries = util.list_entries()
    query = request.GET.get("q")
    if query.upper() in [entry.upper() for entry in entries]:
        return redirect("wiki/" + query)
    else:
        results = [entry for entry in entries if query.upper() in entry.upper()]
        return render(request, "encyclopedia/index.html", {"entries": results})


class NewPage(forms.Form):
    pageTitle = forms.CharField(max_length=150)
    pageContent = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "cols": 5}),
    )


def create(request):
    entries = util.list_entries()
    if request.method == "POST":
        newentry = NewPage(request.POST)
        if newentry.is_valid():
            pageTitle = newentry.cleaned_data["pageTitle"]
            pageContent = newentry.cleaned_data["pageContent"]
            if str(pageTitle).upper() in entries:
                return render(
                    request,
                    "encyclopedia/error.html",
                    {"error": "This entry already exists."},
                )
            else:
                file = open("entries/" + pageTitle + ".md", "w")
                file.write("# " + pageTitle + "\n" + pageContent)
                file.close()
                return redirect("wiki/" + pageTitle)

        else:
            return render(
                request,
                "encyclopedia/newpage.html",
                {
                    "newpage.pageTitle": pageTitle,
                    "newpage.pageContent": pageContent,
                },
            )
    return render(request, "encyclopedia/newpage.html", {"newpage": NewPage()})


# class Edit(forms.Form):
#     textarea = forms.CharField(widget=forms.Textarea(), attrs={"rows": 3, "cols": 5})


def edit(request):
    entries = util.list_entries()
    up_entries = [entry.upper() for entry in entries]

    if request.method == "POST":
        title = request.POST["title"]
        if title.upper() in up_entries:

            return render(request, "encyclopedia/edit.html", {"title": title})
