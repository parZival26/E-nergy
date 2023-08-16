from typing import Any, Dict
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from .models import Casa, Dispositivos, Metas
from .forms import AgregarValoresForm
from django.contrib.auth.mixins import LoginRequiredMixin


from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render


class ListCasas(LoginRequiredMixin, ListView):
    model = Casa
    template_name = 'core/list_casa.html' 
    context_object_name = 'houses'
    
    def get_queryset(self):
        print(Casa.objects.filter(user=self.request.user))
        return Casa.objects.filter(user=self.request.user)
    
class CreateCasas(LoginRequiredMixin, CreateView):
    model = Casa
    fields = ['name', 'areaCuadrada'] 
    template_name = 'core/create_casa.html'  
    success_url = reverse_lazy('home') 

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Agregar Dispositivo'
        return context
    
class UpdateCasas(LoginRequiredMixin, UpdateView):
    model = Casa
    fields = ['name','areaCuadrada'] 
    template_name = 'core/update_casa.html'  # Reemplaza con la ubicación de tu plantilla
    success_url = reverse_lazy('home') 

    def get_queryset(self):
        return Casa.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Casa'
        return context
    
class DeleteCasas(LoginRequiredMixin, DeleteView):
    model = Casa
    template_name = 'core/delete_casa.html'  # Reemplaza con la ubicación de tu plantilla de confirmación de eliminación
    success_url = reverse_lazy('home')  # La URL a la que redirigir después de eliminar una casa

    def get_queryset(self):
        return Casa.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)
    
class DetailCasas(LoginRequiredMixin, DetailView):
    model = Casa
    template_name = 'core/detail_casa.html'  # Reemplaza con la ubicación de tu plantilla de detalles
    context_object_name = 'house'

    def get_queryset(self):
        return Casa.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dispositivos'] = Dispositivos.objects.filter(casa_id=self.kwargs['pk'])
        context['metas'] = Metas.objects.filter(casa_id=self.kwargs['pk'])
        return context
    
  
def agregar_valores_view(request, casa_id):
    casa = get_object_or_404(Casa, pk=casa_id)

    if request.method == 'POST':
        form = AgregarValoresForm(request.POST)
        if form.is_valid():
            valor_kwh = form.cleaned_data['valor_kwh']
            valor_pagar = form.cleaned_data['valor_pagar']
            
            casa.valores_kwh.append(valor_kwh)
            casa.valores_pagar.append(valor_pagar)
            casa.save()
            
            return redirect('detail_casa', casa.pk)  # Reemplaza con la URL correcta
    else:
        form = AgregarValoresForm()

    return render(request, 'core/agregar_valores.html', {'casa': casa, 'form': form})


class ListDispositivosView(LoginRequiredMixin, ListView):
    model = Dispositivos
    template_name = 'core/list_dispositivos.html' 
    context_object_name = 'dispositivos'
    
    def get_queryset(self):
        print(Dispositivos.objects.filter(casa_id=self.kwargs['casa_id']))
        return Dispositivos.objects.filter(casa_id=self.kwargs['casa_id'])
    
class AgregarDispositivoView(CreateView):
    model = Dispositivos
    fields = ['name', 'consumoWPerH', 'horasActivo']
    template_name = 'core/create_casa.html'  


    def form_valid(self, form):
        casa_id = self.kwargs['casa_id']
        casa = Casa.objects.get(pk=casa_id)
        form.instance.casa = casa
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'], context['button'] = ('Agregar Dispositivo', 'Agregar')
        return context
    
    def get_success_url(self):
        return reverse_lazy('detail_casa', kwargs={'pk': self.kwargs['casa_id']})
    
class UpdateDispositivoView(UpdateView):
    model = Dispositivos
    fields = ['name', 'consumoWPerH', 'horasActivo']
    template_name = 'core/update_casa.html'  

    def get_queryset(self):
        casa_id = self.kwargs['casa_id']
        dispositivo_id = self.kwargs['pk']  # Cambia 'dispositivo_id' a 'pk'
        return Dispositivos.objects.filter(casa_id=casa_id, pk=dispositivo_id)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Dispositivo'
        return context
    
    def get_success_url(self):
        return reverse_lazy('detail_casa', kwargs={'pk': self.kwargs['casa_id']})
    
     
class DeleteDispositivoView(DeleteView):
    model = Dispositivos
    template_name = 'core/delete_casa.html'

    def get_queryset(self):
        casa_id = self.kwargs['casa_id']
        dispositivo_id = self.kwargs['pk']
        return Dispositivos.objects.filter(casa_id=casa_id, pk=dispositivo_id)

    def get_success_url(self):
        casa_id = self.kwargs['casa_id']
        return reverse_lazy('detail_casa', kwargs={'pk': casa_id})
    
class AnalisisCasa(LoginRequiredMixin, DetailView):
    model = Casa
    template_name = 'core/analisis_casa.html'
    context_object_name = 'house'

    def get_queryset(self):
        return Casa.objects.filter(user=self.request.user)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['valor_total'] = ecuaciones(self.kwargs['pk'])
        context['dispositivos'] = dispositivos_list(self.kwargs['pk'])
        return context
    

def dispositivos_list(id):
        lista = {}
        matriz = (Dispositivos.objects.values()).filter(casa_id=id)
        cantidad = len(matriz)
        if cantidad == 0:
            lista["x"] = 'No hay Dispositivos'
            return lista.items()
        else:
            for i in range(cantidad):
                dia = matriz[i]['consumoWPerH']*matriz[i]["horasActivo"]
                nombre = matriz[i]["name"]
                lista[nombre] = dia
        return lista.items()

def ecuaciones(id):
    lista = []
    matriz = (Casa.objects.values()).filter(id=id)[0]
    cantidad = len(matriz["valores_pagar"])
    if cantidad == 0:
        lista = ["No hay datos para realizar el analisis"]
    else:
        for i in range(cantidad):
            valor = round(matriz['valores_pagar'][i]/matriz['valores_kwh'][i], 2)
            lista.append(valor)
            if i == 0:
                cache = valor
                continue
            elif cache == valor:
                lista.append("Neutro")
            elif cache < valor:
                lista.append("Subio el kwh")
            else:
                lista.append("Bajo el kwh")
            cache = valor
    return lista

class ListMetasView(LoginRequiredMixin, ListView):
    model = Metas
    template_name = 'core/list_metas.html' 
    context_object_name = 'metas'
    
    def get_queryset(self):
        print(Metas.objects.filter(casa_id=self.kwargs['casa_id']))
        return Metas.objects.filter(casa_id=self.kwargs['casa_id'])
    
class AgregarMetaView(CreateView):
    model = Metas
    template_name = 'core/create_casa.html'
    fields = ['description']

    def form_valid(self, form):
        casa_id = self.kwargs['casa_id']
        casa = Casa.objects.get(pk=casa_id)
        form.instance.casa = casa
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'], context['button']= ('Agregar Meta', "Agregar")
        return context
    
    def get_success_url(self):
        return reverse_lazy('detail_casa', kwargs={'pk': self.kwargs['casa_id']})
    
class UpdateMetaView(UpdateView):
    model = Metas
    fields = ['description']
    template_name = 'core/update_casa.html'  

    def get_queryset(self):
        casa_id = self.kwargs['casa_id']
        meta_id = self.kwargs['pk']  # Cambia 'dispositivo_id' a 'pk'
        return Metas.objects.filter(casa_id=casa_id, pk=meta_id)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Meta'
        return context
    
    def get_success_url(self):
        return reverse_lazy('detail_casa', kwargs={'pk': self.kwargs['casa_id']})
    
class DeleteMetaView(DeleteView):
    model = Metas
    template_name = 'core/delete_casa.html'

    def get_queryset(self):
        casa_id = self.kwargs['casa_id']
        meta_id = self.kwargs['pk']
        return Metas.objects.filter(casa_id=casa_id, pk=meta_id)

    def get_success_url(self):
        casa_id = self.kwargs['casa_id']
        return reverse_lazy('detail_casa', kwargs={'pk': casa_id})
    

class recomendaciones_casas(LoginRequiredMixin, DetailView):
    model = Casa
    template_name = 'core/recomendaciones_casa.html'
    context_object_name = 'house'

    def get_queryset(self):
        return Casa.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dispositivos'] = Dispositivos.objects.filter(casa_id=self.kwargs['pk'])
        context['Max'] = maxi(self.kwargs['pk'])
        return context
    

def maxi(id):
    lista = {}
    matriz = (Dispositivos.objects.values()).filter(casa_id=id)
    cantidad = len(matriz)
    if cantidad == 0:
        lista["Maximo"] = "No hay dispositivos"
    else:
        for i in range(cantidad):
            dia = matriz[i]['consumoWPerH']*matriz[i]["horasActivo"]
            nombre = matriz[i]["name"]
            lista[nombre] = dia
        maximo = max(lista)
        lista["Maximo"] = maximo
    return lista