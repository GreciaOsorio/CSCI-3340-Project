from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from .models import UserProfile, Project
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect #check why we have to keep using these if they are supposed to be automatic 


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

#helper
def prepare_dashboard_context(user, is_manager):
    if is_manager:
        projects = Project.objects.filter(p_manager=user)
        project_heading = "(Manager) Your projects:"
        template_name = 'managerDashboard.html'
    else:
        projects = Project.objects.filter(p_members=user)
        project_heading = "(Teammate) Your projects:"
        template_name = 'teammateDash.html'
    
    context = {
        'name': user.username,
        'projects': projects,
        'project_heading': project_heading,
    }
    return context, template_name

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
                #call function here for creating user context 
                login(request, user)
                messages.success(request, f'Successful login for: {username}.')
                
                # Determine user type and prepare dashboard
                user_type = user.userprofile.user_type
                is_manager = user_type == 'manager' #checks if user is manager otherwise itll 'else' to teammate 
                context, template_name = prepare_dashboard_context(request.user, is_manager)
                            # If our user w/ entered info exists in our database...
                return render(request, template_name, context)
            else: # Same here, our login success message shows in Django admin (make sure to refresh page).

                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
