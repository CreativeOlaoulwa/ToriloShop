from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Welcome to My Django App!</h1>')

def about(request):
    return HttpResponse('<h1>About My Django App</h1><p>This is a simple Django application.</p>')

def hello_world(request):
    return HttpResponse('<h1>Hello, World!</h1>')