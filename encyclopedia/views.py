import markdown2
import random

from django.shortcuts import render, redirect
from django.core.files.storage import default_storage

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
        "title": title,
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
        return render(request, "encyclopedia/search.html", {
            "query": q,
            "results": matching_entries            
        })
    
def create(request):
    if request.method == "POST":
        title = request.POST.get('title', '').strip()
        content = request.POST.get('textbox', '').strip()

        if not title:
            return render(request, "encyclopedia/create.html", {
                "empty_title": "Title field cannot be empty",
                "title": title,
                "content": content   
            })
        
        elif not content:
            return render(request, "encyclopedia/create.html", {
                "content_error": "Content field cannot be empty",
                "title": title,
                "content": content      
            })
        
        elif util.get_entry(title):
            return render(request, "encyclopedia/create.html", {
                "exists_error": "This title already exists",
                "title": title,
                "content": content              
            })
        
        util.save_entry(title, content)

        entry = util.get_entry(title)

        entry_html = markdown2.markdown(entry)

        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry_html
        })

    return render(request, "encyclopedia/create.html")

def edit(request, title):
    if request.method == "POST":
        new_title = request.POST.get('title', '').strip()
        raw_content = request.POST.get('textbox', '')
        content = "\n".join(line.rstrip() for line in raw_content.splitlines()).strip()

        if not new_title:
            return render(request, "encyclopedia/edit.html", {
                "empty_title": "Title field cannot be empty",
                "title": title,
                "content": content   
            })
        
        elif not content:
            return render(request, "encyclopedia/edit.html", {
                "content_error": "Content field cannot be empty",
                "title": new_title,
                "content": content      
            })
        
        elif util.get_entry(new_title) and new_title != title:
            return render(request, "encyclopedia/edit.html", {
                "exists_error": "This title already exists",
                "title": title,
                "content": content              
            })
        
        filename = f"entries/{title}.md"
        default_storage.delete(filename)

        util.save_entry(new_title, content)

        return redirect(f"/{new_title}")

    content = util.get_entry(title)
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def random_entry(request):
    entries = util.list_entries()

    random_entry = random.choice(entries)

    return redirect(f"/{random_entry}")