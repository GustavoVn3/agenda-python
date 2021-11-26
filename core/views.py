from django.shortcuts import render, HttpResponse
from core.models import Evento

# Create your views here.
def event(request):
    tit = Evento.objects.all()
    dados = {'eventos':tit}
    return render(request, 'agenda.html', dados)