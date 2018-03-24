from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def team(request):
    return render(request, 'team.html')


def contact_us(request):
    return render(request, 'contact_us.html')
