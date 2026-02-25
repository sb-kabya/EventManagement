from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    path('dashboard/', views.DashboardRedirectView.as_view(),
         name='dashboard_redirect'),
    path('dashboard/admin/', views.AdminDashboardView.as_view(),
         name='admin_dashboard'),
    path('dashboard/organizer/', views.organizer_dashboard,
         name='organizer_dashboard'),
    path('dashboard/participant/', views.ParticipantDashboardView.as_view(),
         name='participant_dashboard'),
    path('events/', views.event_list, name='event_list'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event/add/', views.add_event, name='event_add'),
    path('event/edit/<int:pk>/', views.update_event, name='update_event'),
    path('event/delete/<int:pk>/', views.delete_event, name='event_delete'),
    path('event/rsvp/<int:pk>/', views.rsvp_event, name='rsvp_event'),
    path('activate/<int:user_id>/',
         views.activate_account, name='activate_account'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

]
