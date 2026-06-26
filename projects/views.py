from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import (DetailView, UpdateView, CreateView, ListView)

from utils.mixins import ProjectOwnerRequiredMixin
from . import constants
from .forms import ProjectCreateForm
from .models import Project

User = get_user_model() 


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'projects/create-project.html'
    form_class = ProjectCreateForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context


class ProjectUpdateView(LoginRequiredMixin, ProjectOwnerRequiredMixin,
                        UpdateView):
    model = Project
    template_name = 'projects/create-project.html'
    form_class = ProjectCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project-list.html'
    paginate_by = constants.PROJECTS_PER_PAGE

    def get_queryset(self):
        return Project.objects.select_related('owner').prefetch_related('participants').order_by('-created_at')


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project-details.html'


class ProjectFavoriteListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/favorite_projects.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return self.request.user.favorites.select_related(
            'owner').prefetch_related('participants')


class ToggleFavoriteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk'])
        user = request.user
        if in_favorites := user.favorites.filter(id=project.id).exists():
            user.favorites.remove(project)
        else:
            user.favorites.add(project)
        return JsonResponse({'status': 'ok', 'favorited': not in_favorites})


class ToggleComplete(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk'])
        user = request.user

        if ((project.owner == user or user.is_staff)
                and project.status == constants.STATUS_OPEN):
            project.status = constants.STATUS_CLOSED
            project.save(update_fields=['status'])
            return JsonResponse(
                {"status": "ok", "project_status": constants.STATUS_CLOSED})
        return JsonResponse(
            {"status": "error", "project_status": constants.STATUS_OPEN})


class ToggleParticipate(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk'])
        user = request.user
        if participant := project.participants.filter(id=user.id).exists():
            project.participants.remove(user)
        else:
            project.participants.add(user)
        return JsonResponse({"status": "ok", "participant": not participant})
