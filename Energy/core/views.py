from .models import Casa, Dispositivos
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
        context['titulo'] = 'Agregar Dispositivo'
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
        return context

def ecuaciones(id):

    matriz = Casa.objects.values()
    matriz = matriz[id-1]
    valor_total = sum(matriz['valores_pagar'])/sum(matriz['valores_kwh'])
    return round(valor_total, 2)