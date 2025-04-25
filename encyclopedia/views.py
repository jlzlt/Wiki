import markdown2

from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)

    if not entry:
        return render(request, "encyclopedia/notfound.html")

    entry_html = markdown2.markdown(entry)

    return render(request, "encyclopedia/entry.html", {
        "title": title.capitalize(),
        "entry": entry_html
    })