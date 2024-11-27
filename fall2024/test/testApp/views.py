from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect # check why we have to keep using these if they are supposed to be automatic 
from django.utils import timezone
from .forms import SignUpForm, LoginForm
from .models import UserProfile, Project, Task

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
            login(request, user)
            if user_type == 'manager':
                    return redirect('managerDash')  # Redirect to manager dashboard
            elif user_type == 'teammate':
                    return redirect('teammateDash')  # Redirect to teammate dashboard
            else: 
                return redirect('home') # Replace this with whatever screen we want to initially show our user after they signup.
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'signup.html', context)

# Helper for login_view
def prepare_dashboard_context(user, is_manager):
    if is_manager:
        projects = Project.objects.filter(p_manager=user)
        project_heading = "Your projects:"
        template_name = 'managerDash.html'
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
@ensure_csrf_cookie # Ensures token is available for form; helps if you're doing a lot of testing. 
def login_view(request):
    if request.method == 'POST': 
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Call function here for creating user context.
                login(request, user)
                messages.success(request, f'Successful login for: {username}.')
                # Determine user type and redirect to their dashboard.
                user_type = user.userprofile.user_type
                if user_type == 'manager':
                    return redirect('managerDash')  # Redirect to manager dashboard
                elif user_type == 'teammate':
                    return redirect('teammateDash')  # Redirect to teammate dashboard
                
            else: # Same here, our login success message shows in Django admin (make sure to refresh page).
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def manager_dashboard(request):
    if request.user.userprofile.user_type != 'manager':
        raise PermissionDenied
    context, template_name = prepare_dashboard_context(request.user, True)
    return render(request, template_name, context)


@login_required
def teammate_dashboard(request):
    if request.user.userprofile.user_type != 'teammate':
        raise PermissionDenied
    context, template_name = prepare_dashboard_context(request.user, False)
    return render(request, template_name, context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('home') 


# All Cubby users can view their project lists and specific project details.
@login_required
def project_list_view(request):
    if request.user.userprofile.user_type == 'manager':
        projects = Project.objects.filter(p_manager=request.user)
    else:
        projects = Project.objects.filter(p_members=request.user)
    
    context = {
        'projects': projects,
        'user_type': request.user.userprofile.user_type
    }
    return render(request, 'projectList.html', context)

@login_required
def project_detail_view(request, id):
    if request.user.userprofile.user_type == 'manager':
        project = get_object_or_404(Project, id=id, p_manager=request.user)
    else:
        project = get_object_or_404(Project, id=id, p_members=request.user)
    
    tasks = project.tasks.all()
    context = {
        'project': project,
        'tasks': tasks,
        'user_type': request.user.userprofile.user_type
    }
    return render(request, 'projectDetail.html', context)


# Unique to managers: can create, update, and delete projects + tasks.
@login_required
def create_project_view(request):
    if request.user.userprofile.user_type != 'manager':
        raise PermissionDenied
    
    # Get all users who are teammates.
    available_teammates = User.objects.filter(
        userprofile__user_type='teammate'
    )
    
    if request.method == 'POST':
        project = Project.objects.create(
            p_name=request.POST['name'],
            p_description=request.POST['description'],
            p_due_date=request.POST['due_date'],
            p_manager=request.user
        )
        project.p_members.set(request.POST.getlist('members'))

        # Takes us to view the newly-created project info from the "Project Detail" page.
        return redirect('project_detail', id=project.id)
    
    context = {
        'available_teammates': available_teammates
    }
    return render(request, 'createProject.html', context)

# If a project member is removed, their tasks should disappear (need to add this).
@login_required
def update_project_view(request, id):
    if request.user.userprofile.user_type != 'manager':
        raise PermissionDenied
    
    project = get_object_or_404(Project, id=id, p_manager=request.user)

    # Get all users who are teammates.
    available_teammates = User.objects.filter(
        userprofile__user_type='teammate'
    )

    # If someone is removed from a project, their tasks should become unassigned (no teammate assigned to task).
    if request.method == 'POST':
        project.p_name = request.POST['name']
        project.p_description = request.POST['description']
        project.p_due_date = request.POST['due_date']
        # Debating if the two following lines are necessary...
        project.p_modified_date = timezone.now()
        project.save()
        project.p_members.set(request.POST.getlist('members'))

        return redirect('project_detail', id=project.id)
    
    context = {
        'project': project,
        'members': User.objects.all(),
        'available_teammates': available_teammates
    }

    return render(request, 'updateProject.html', context)

@login_required
def create_task_view(request, id):
    if request.user.userprofile.user_type != 'manager':
        raise PermissionDenied
    
    project = get_object_or_404(Project, id=id, p_manager=request.user)
    # Show all the users who are currently working on the task's related project.
    project_members = project.p_members.all()

    if request.method == 'POST':
        task = Task.objects.create(
            project=project,
            t_name=request.POST['name'],
            t_description=request.POST['description'],
            t_due_date=request.POST['due_date'],
            t_manager=request.user
        )
        task.t_assignees.set(request.POST.getlist('assignees'))

        return redirect('project_detail', id=project.id)
    
    context = {
        'project': project,
        'project_members': project_members
    }
    return render(request, 'createTask.html', context)

@login_required
def update_task_view(request, id, t_id):
    if request.user.userprofile.user_type != 'manager':
        raise PermissionDenied
    
    project = get_object_or_404(Project, id=id, p_manager=request.user)
    task = get_object_or_404(Task, id=t_id, project=project)

    project_members = project.p_members.all()
    
    if request.method == 'POST':
        task.t_name = request.POST['name']
        task.t_description = request.POST['description']
        task.t_due_date = request.POST['due_date']
        # Check if these 2 lines need to be left in.
        task.t_modified_date = timezone.now()
        task.save()
        task.t_assignees.set(request.POST.getlist('assignees'))
        
        return redirect('project_detail', id=project.id)
    
    context = {
        'project': project,
        'task': task,
        'project_members': project_members
    }
    return render(request, 'updateTask.html', context)

@login_required
def delete_project_view(request, id):
    # Only managers can delete projects.
    if request.user.userprofile.user_type != 'manager':
        raise PermissionDenied
    
    # Ensure the user is the manager of this project.
    project = get_object_or_404(Project, id=id, p_manager=request.user)
    
    if request.method == 'POST':
        project_name = project.p_name
        # Delete the project and related tasks.
        project.delete()
        messages.success(request, f'Project "{project_name}" has been deleted.')
        # Once deleted, return to the user's dashboard/project list page since current project has been deleted.
        return redirect('project_list')
    
    # Show deletion confirmation page.
    return render(request, 'deleteProject.html', {'project': project})

@login_required
def delete_task_view(request, id, t_id):
    # Only managers can delete tasks.
    if request.user.userprofile.user_type != 'manager':
        raise PermissionDenied
    
    # Ensure the user is the manager of the project containing this task.
    project = get_object_or_404(Project, id=id, p_manager=request.user)
    task = get_object_or_404(Task, id=t_id, project=project)
    
    if request.method == 'POST':
        task_name = task.t_name
        # Delete the task.
        task.delete()
        messages.success(request, f'Task "{task_name}" has been deleted.')
        # Once deleted, return to the deleted task's project page.
        return redirect('project_detail', id=project.id)
    
    return render(request, 'deleteTask.html', {'project': project, 'task': task})

# Unique to teammates (a.k.a project members, task assignees): can update the status of their assigned task(s).
# what needs to be done here: update_task_status_view (for project members/assignees)
# add url for it, too