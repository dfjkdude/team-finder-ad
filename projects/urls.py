from django.urls import path

from . import views

app_name = 'projects'
urlpatterns = [
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='edit'),
    path('create-project/', views.ProjectCreateView.as_view(), name='create'),
    path('list/', views.ProjectListView.as_view(), name='list'),
    path('favorites/', views.ProjectFavoriteListView.as_view(),
         name='favorites_list'),
    path('<int:pk>/toggle-favorite/', views.ToggleFavoriteView.as_view(),
         name='toggle_favorite'),
    path('<int:pk>/complete/', views.ToggleComplete.as_view(),
         name='toggle_complete'),
    path('<int:pk>/toggle-participate/', views.ToggleParticipate.as_view(),
         name='toggle_participate')
]
