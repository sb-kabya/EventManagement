
from django.urls import path
from . import views
app_name = 'events'

urlpatterns = [
    path('event_list/', views.event_list, name='event_list'),  # for list
    path('add/', views.add_event, name='event_add'),  # for create
    path('event/<int:pk>/edit/', views.update_event,
         name='update_event'),  # for update
    path('event/<int:pk>/delete/', views.delete_event,
         name='event_delete'),  # for delete
    path('', views.dashboard, name='dashboard'),  # dashboard
    path('<int:pk>/', views.event_detail, name='event_detail'),

]
