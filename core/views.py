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
def submit_evento(request):
    if request.POST:
        id = request.POST.get('id')
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data_evento = request.POST.get('data_evento')
        local = request.POST.get('local')
        usuario = request.user
        if id:
            evento = Evento.objects.get(id=id)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.local = local
                evento.save()
        else:
            Evento.objects.create(titulo=titulo,
                                  descricao=descricao,
                                  data_evento=data_evento,
                                  local=local,
                                  usuario=usuario)
    return redirect('/')


@login_required(login_url='/login/')
def eventos(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)


@login_required(login_url='/login/')
def delete_eventos(request, id_evento):
    evento = Evento.objects.get(id=id_evento)
    usuario = request.user
    if evento.usuario == usuario:
        evento.delete()
    return redirect('/')


@login_required(login_url='/login/')
def event(request):
    usuario = request.user
    tit = Evento.objects.filter(usuario=usuario)
    dados = {'eventos': tit}
    return render(request, 'agenda.html', dados)
