from django.shortcuts import render


def home(request):
    return render(request, "personal/reg.html", {})


def about(request):
    return render(request, "personal/about.html")