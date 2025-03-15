from django.shortcuts import render

def ShowLogs(request):
    return render(request, 'logs.html')