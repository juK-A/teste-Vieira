from django.shortcuts import render, redirect, get_object_or_404
from tarefas.models import Responsible, Activities, Profile, DiscordLinkToken
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from tarefas.forms import ActivitiesModelForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib import messages



@method_decorator(login_required(login_url='login'), name='dispatch')
class ActivitiesListView(ListView):
    model = Activities
    template_name = 'list_activities.html'
    context_object_name = 'activities_list'
    paginate_by = 3

    def get_queryset(self):
        base_queryset = Activities.objects.filter(
            owner=self.request.user, 
            deleted_at__isnull=True
        )
        status = self.request.GET.get('status', 'all')
        if status == 'completed':
            return base_queryset.filter(done=True)
        elif status == 'pending':
            return base_queryset.filter(done=False)
        else:
            return base_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', 'all')
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class ActivitiesDetailView(DetailView):
    model = Activities
    template_name = 'details_activities.html'

@login_required(login_url='login')
def complete_activity_view(request, pk):
    activity = get_object_or_404(Activities, pk=pk)
    activity.done = True
    activity.save()
    return redirect('list_activities')

@method_decorator(login_required(login_url='login'), name='dispatch')
class NewActivitiesCreateView(CreateView):
    model = Activities
    form_class = ActivitiesModelForm
    template_name = 'new_activities.html'
    success_url = reverse_lazy('list_activities')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responsible'] = Responsible.objects.all()
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class ActivitiesUpdateView(UpdateView):
    model = Activities
    form_class = ActivitiesModelForm
    template_name = 'update_activities.html'

    def get_success_url(self):
        return reverse_lazy('details_activities', kwargs={'pk': self.object.pk})

@method_decorator(login_required(login_url='login'), name='dispatch')
class ActivitiesDeleteView(DeleteView):
    model = Activities
    template_name = 'delete_activities.html'
    success_url = reverse_lazy('list_activities')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.deleted_at = timezone.now()
        self.object.deleted_by = request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

@login_required(login_url='login')
def link_discord_view(request, token):
    try:
        link_token = DiscordLinkToken.objects.get(token=token, is_used=False)
    except DiscordLinkToken.DoesNotExist:
        messages.error(request, "Este link de vinculação é inválido ou já expirou.")
        return redirect('list_activities')

    if request.method == 'POST':
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        profile.discord_id = link_token.user_discord_id
        profile.save()

        link_token.is_used = True
        link_token.save()

        messages.success(request, "Sua conta do Discord foi vinculada com sucesso!")
        return redirect('list_activities')

    context = {
        'token': token,
    }
    return render(request, 'link_discord_confirm.html', context)