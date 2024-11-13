from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from .models import UserProfile
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect



# Create your views here.
def home(request):
    return render(request, 'home.html', {})

@csrf_protect
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create instance of a user.
            user = form.save()

            # Get or create the appropriate group ("Project Managers" or "Project Teammates"), and add the user to the group.
            user_type = form.cleaned_data.get('user_type')
            group_name = 'Project Managers' if user_type == 'manager' else 'Project Teammates'
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
            
            # Create associated UserProfile for user.
            UserProfile.objects.create(
                user=user,
                user_type=user_type
            )

            # Signup success message shown in Django admin.
            messages.success(request, 'Account created successfully!')
            return redirect('home') # Replace this with whatever screen we want to initially show our user after they signup.
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'signup.html', context)


from .models import Project
@csrf_protect
@ensure_csrf_cookie #ensures token is available for form, helps if youre doing a lot of testing 
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None: 
                # This messes with your Django admin login (logs you out), but why?
                # login(request, user)
                messages.success(request, f'Successful login for: {username}.')
                
                login(request, user)

                user_type = user.userprofile.user_type
                
                if user_type == 'manager':
                    user = request.user
                    projects = Project.objects.filter(p_manager=user)
                    project_heading = "(Manager) Your projects:"
                    context = {
                    'name': user.username,
                    'projects': projects,
                    'project_heading': project_heading,
                    }
                    return render(request, 'managerDashboard.html', context)
                
                else:     
                    user = request.user
                    projects = Project.objects.filter(p_members=user)
                    project_heading = "(Teammate) Your projects:"
                    context = {
                    'name': user.username,
                    'projects': projects,
                    'project_heading': project_heading,
                    } 
                    return render(request, 'teammateDash.html', context)
                            # If our user w/ entered info exists in our database...
            else: # Same here, our login success message shows in Django admin (make sure to refresh page).
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'login.html', context)

# @csrf_protect
# def dashboard(request):
#     user = request.user
#     user_type = user.userprofile.user_type
    
#     context = {
#         'name': user.username,
#         'projects': projects,
#         'project_heading': project_heading,
#     }
    
#     if user_type == 'manager':
#         projects = Project.objects.filter(p_manager=user)
#         project_heading = "(Manager) Your projects:"
#         return render(request, 'managerDashboard.html', context)
#     else:
#         projects = Project.objects.filter(p_members=user)
#         project_heading = "(Teammate) Your projects:"
#         return render(request, 'teammateDashboard.html', context)


# def managerDashboard(request):
#     user = request.user
#     projects = Project.objects.filter(p_manager=user)
#     project_heading = "(Manager) Your projects:"

#     context = {
#         'name': user.username,
#         'projects': projects,
#         'project_heading': project_heading,
#     }
#     return render(request, 'managerDashboard.html', context)


# def teammateDashboard(request):
#     user = request.user
#     projects = Project.objects.filter(p_members=user)
#     project_heading = "(Teammate) Your projects:"

#     context = {
#         'name': user.username,
#         'projects': projects,
#         'project_heading': project_heading,
#     }
#     return render(request, 'teammateDashboard.html', context)

