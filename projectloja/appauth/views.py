from django.shortcuts import render


def a(request):
    return render(request,'auth/a.html')