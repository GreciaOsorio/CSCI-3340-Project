# from django.urls import path, include
# #dot means to look within this directory for the views file
# from . import views

# #This is where you will keep adding paths, the controller will look here for access
# urlpatterns = [
#     path('', views.home, name = 'home'),
#     #path('login/', views.login_user, name = 'Login'),
#     #path('logout/', views.logout_user, name = 'Logout'),
#     path('Sign Up/', views.signup_view, name = 'signup'),
#     path('Log In/', views.login_view, name = 'login'),

# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('managerDash/', views.manager_dashboard, name='managerDash'), 
    path('teammateDash/', views.teammate_dashboard, name = 'teammateDash'),
    path('projects/', views.project_list_view, name='project_list'),
    path('projects/<int:id>/', views.project_detail_view, name='project_detail'),
    path('projects/manager/create/', views.create_project_view, name='create_project'),
    path('projects/manager/<int:id>/update/', views.update_project_view, name='update_project'),
    path('projects/manager/<int:id>/tasks/create/', views.create_task_view, name='create_task'),
    path('projects/manager/<int:id>/tasks/<int:t_id>/update/', views.update_task_view, name='update_task'),
    path('projects/<int:id>/delete/', views.delete_project_view, name='delete_project'),
    path('projects/<int:id>/tasks/<int:t_id>/delete/', views.delete_task_view, name='delete_task'),
    # This is pending: path('projects/teammate/<int:id>/tasks/<int:t_id>/update/', views.update_task_status_view, name='update_task_status')
    path('projects/teammate/<int:id>/tasks/<int:t_id>/update/', views.update_task_status_view, name='update_task_status'),


]
