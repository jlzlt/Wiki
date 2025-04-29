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

def search(request):
    q = request.GET.get('q', '').strip()

    entry = util.get_entry(q)
    all_entries = util.list_entries()

    if entry is not None:
        # If search query is available as an entry generate page
        entry_html = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry.html", {
            "title": q.capitalize(),
            "entry": entry_html
        })
    else:
        # Handle partial matches (substring search)
        matching_entries = [e for e in all_entries if q.lower() in e.lower()]
        print(matching_entries)
        return render(request, "encyclopedia/search.html", {
            "query": q,
            "results": matching_entries            
        })