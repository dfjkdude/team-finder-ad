from django.contrib.auth.views import LoginView
from django.urls import path, reverse_lazy

from .forms import UserLoginForm
from .views import (UserListView, UserCreateView,
                    UserDetailView,
                    UserUpdateView, PasswordChangeView,
                    logout_view)

app_name = 'users'
urlpatterns = [
    path('<int:pk>/', UserDetailView.as_view(), name='user'),
    path('login/', LoginView.as_view(template_name='users/login.html',
                                     success_url=reverse_lazy('projects:list'),
                                     form_class=UserLoginForm
                                     ),
         name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('change-password/', PasswordChangeView.as_view(),
         name='change_password'),
    path('list/', UserListView.as_view(), name='list'),
    path('edit-profile/', UserUpdateView.as_view(), name='edit')
]
