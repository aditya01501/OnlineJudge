from django.shortcuts import render

# Create your views here.


def HomePage(request): 
    USER = request.user
    context = {'USER' : USER}
    return render(request, 'UserHomePage.html', context)   