from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
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
                    return redirect('managerDash')  # Redirect to manager dashboard.
            elif user_type == 'teammate':
                    return redirect('teammateDash')  # Redirect to teammate dashboard.
            else: 
                return redirect('home') # Replace this with whatever screen we want to initially show our user after they signup.
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'signup.html', context)

# Helper for login_view.
def prepare_dashboard_context(user, is_manager):
    if is_manager:
        projects = Project.objects.filter(p_manager=user)
        project_heading = "Your projects:"
        template_name = 'managerDash.html'
    else:
        projects = Project.objects.filter(p_members=user)
        project_heading = "Your projects:"
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
                    return redirect('managerDash')  # Redirect to manager dashboard.
                elif user_type == 'teammate':
                    return redirect('teammateDash')  # Redirect to teammate dashboard.
                
            else: # Same here, our login success message shows in Django admin (make sure to refresh page).
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

# Managers and teammates have slightly different dashboards because only managers can choose to create a new project.
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
    # Clear all messages.
    storage = get_messages(request)
    for _ in storage:  # Iterate through to clear.
        pass
    logout(request)
    return redirect('home') 

# All Cubby users can view their project lists (used during testing) and specific project details.
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
    project = get_object_or_404(Project, id=id)
    
    # Check if the user is a member of the project.
    if request.user not in project.p_members.all() and request.user != project.p_manager:
        raise PermissionDenied
    # Is user a project manager or teammate/assignee?
    user_type = request.user.userprofile.user_type
    tasks = project.tasks.all()
    
    context = {
        'project': project,
        'tasks': tasks,
        'user_type': user_type,
        'current_user': request.user
    }
    return render(request, 'projectDetail.html', context)

# Unique to managers: can create, update, and delete projects + tasks.
@login_required
def create_project_view(request):
    if request.user.userprofile.user_type != 'manager':
        raise PermissionDenied
    
    # Get all available users who are teammates.
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

# When updating a project, we take into consideration removing teammates who have tasks assigned to them.
# If the assignee was the only person working on a task, then their task becomes unassigned.
# If the assignee was working on a task with other people, and there will still be remaining assigness after their removal, then they are simply removed from the assignee list.
@login_required
def update_project_view(request, id):
    if request.user.userprofile.user_type != 'manager':
        raise PermissionDenied
    
    project = get_object_or_404(Project, id=id, p_manager=request.user)
    
    # Get all users who are teammates.
    available_teammates = User.objects.filter(
        userprofile__user_type='teammate'
    )
    
    if request.method == 'POST':
        project.p_name = request.POST['name']
        project.p_description = request.POST['description']
        project.p_due_date = request.POST['due_date']
        project.p_modified_date = timezone.now()
        project.save()

        # Get the current (before updating the project) and new members, which allows for us to determine members to be removed.
        current_members = set(project.p_members.all())
        new_member_ids = request.POST.getlist('members')
        new_members = set(User.objects.filter(id__in=new_member_ids))
        removed_members = current_members - new_members
        
        project.p_members.set(new_members)
        
        # Handle any potential tasks that removed members may have been assigned to.
        if removed_members:
            for task in project.tasks.all():
                # Get current task assignees.
                current_assignees = set(task.t_assignees.all())
                # Remove the task assignees that were removed from the project.
                removed_task_assignees = current_assignees.intersection(removed_members)
                # Update task assignee list.
                if removed_task_assignees:
                    task.t_assignees.remove(*removed_task_assignees)
                    task.t_modified_date = timezone.now()
                    task.save()
        
        return redirect('project_detail', id=project.id)
    
    context = {
        'project': project,
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
        # Check if assignees were selected, since assignees are optional.
        assignees = request.POST.getlist('assignees')
        if assignees:
            task.t_assignees.set(assignees)
        
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
        task.t_modified_date = timezone.now()

        # Handle assignees.
        assignees = request.POST.getlist('assignees')
        if assignees:
            # If there are assignees are selected, update them.
            task.t_assignees.set(assignees)
        else:
            # If no assignees are selected, clear the current assignees, which makes task unassigned.
            task.t_assignees.clear()
    
        task.save()
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
        return redirect('managerDash')
    
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
@login_required
def update_task_status_view(request, id, t_id):
    # Ensure the current user is a teammate.
    if request.user.userprofile.user_type != 'teammate':
        raise PermissionDenied

    # Get the project and task, ensuring the current user has access.
    project = get_object_or_404(Project, id=id, p_members=request.user)
    task = get_object_or_404(Task, id=t_id, project=project)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES).keys():
            task.t_status = new_status
            task.save()
            messages.success(request, f'Status for task "{task.t_name}" updated to "{new_status}".')
        else:
            messages.error(request, "Invalid status choice.")
        return redirect('project_detail', id=project.id)
    
    raise PermissionDenied