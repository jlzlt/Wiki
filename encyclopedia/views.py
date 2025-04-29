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
            "title": title.capitalize(),
            "entry": entry_html
        })

    return render(request, "encyclopedia/create.html")