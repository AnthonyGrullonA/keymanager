from django.shortcuts import render

def index(request):
    context = {
        'page_title': 'Inicio | Keymanager',
        'favicon_path': 'assets/img/kaiadmin/favicon.ico',
    }
    return render(request, "core/index.html", context)
