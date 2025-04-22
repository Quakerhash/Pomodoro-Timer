from django.shortcuts import render, redirect

 
def HOME(request):
    return render(request, 'home.html')
def ABOUT(request):
    return render(request, 'about.html')
def ss(request):
    return render(request, 'Studys.html')
def Timer(request):
    return render(request, 'Timer.html')
def Progress(request):
    return render(request, 'progress.html')
