from django.shortcuts import render

from . import util

import markdown2

entries = util.list_entries()


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": entries})


def title(request, title):
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
