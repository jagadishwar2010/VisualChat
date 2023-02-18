from django.shortcuts import render

# Create your views here.


def lobby(request):
    return render(request, 'app/lobby.html')


def room(request):
    return render(request, 'app/room.html')
