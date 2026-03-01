from django.shortcuts import render

def learn_page(request):
    return render(request, "learning/learn.html")