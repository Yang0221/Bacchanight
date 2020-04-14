from django.shortcuts import render

def home(request):
    return render (request , 'pages/home.html')

def contact(request):
    return render (request , 'pages/contact.html')

def handler404(request ,exception):
    return render (request , 'errors/404.html' , {'error' : exception} , status=404)
