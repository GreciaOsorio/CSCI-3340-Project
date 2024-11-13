from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import CreateUserForm
#from .filters import OderFilter

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

#def login_user(request):
#   pass

#def logout_user(request):
#    pass

def signup(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid:
            form.save()



    context= {'form': form}
    return render (request, 'signup.html', context)