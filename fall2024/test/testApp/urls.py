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
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    #path('dashboard/', views.dashboard, name='dashboard'),  # New dashboard URL
    # path('managerDash/', views.managerDashboard, name='managerDash'), 
    # path('teammateDash/', views.teammateDashboard, name = 'teammateDash')
]
