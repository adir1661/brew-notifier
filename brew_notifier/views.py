from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse


def homePageView(request):
    return HttpResponse("<a href=\"/admin\">go to admin</a>")