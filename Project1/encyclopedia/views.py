from tkinter import Entry
from django.shortcuts import redirect, render

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
            {"content": content},
        )
    else:
        return render(request, "encyclopedia/error.html")


def search(request):
    entries = util.list_entries()
    query = request.GET.get("q")
    if query.upper() in [entry.upper() for entry in entries]:
        return redirect("wiki/" + query)
    else:
        results = [entry for entry in entries if query.upper() in entry.upper()]
        return render(request, "encyclopedia/index.html", {"entries": results})
