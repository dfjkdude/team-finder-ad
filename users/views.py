from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView as PasswordChange
from django.shortcuts import reverse, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .forms import UserCreateForm, UserUpdateForm

User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = User.objects.all()
        user = self.request.user
        filter_param = self.request.GET.get('filter')

        if filter_param == 'owners-of-favorite-projects':
            favorites = user.favorites.all()
            authors_ids = favorites.values_list('owner', flat=True)
            queryset = User.objects.filter(id__in=authors_ids)
        elif filter_param == 'owners-of-participating-projects':
            participates = user.participated_projects.all()
            authors_ids = participates.values_list('owner', flat=True)
            queryset = User.objects.filter(id__in=authors_ids)
        elif filter_param == 'interested-in-my-projects':
            projects = user.owned_projects.all()
            queryset = User.objects.filter(favorites__in=projects)
        elif filter_param == 'participants-of-my-projects':
            projects = user.owned_projects.all()
            ids = projects.values_list('participants', flat=True)
            queryset = User.objects.filter(id__in=ids).distinct()
        return queryset


class UserCreateView(CreateView):
    template_name = 'users/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('users:login')


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user-details.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/edit_profile.html'
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        user = self.request.user
        return user

    def get_success_url(self):
        return reverse('users:user',
                       kwargs={'pk': self.request.user.pk})


class PasswordChangeView(LoginRequiredMixin, PasswordChange):
    template_name = 'users/change_password.html'

    def get_success_url(self):
        return reverse('users:user', kwargs={'pk': self.request.user.pk})


def logout_view(request):
    logout(request)
    return redirect('projects:list')
