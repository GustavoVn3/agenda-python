from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
        else:
            messages.error(request, "Email ou senha inválidos")
    return redirect('/')

@login_required(login_url='/login/')
def event(request):
    usuario = request.user
    tit = Evento.objects.filter(usuario=usuario)
    dados = {'eventos':tit}
    return render(request, 'agenda.html', dados)