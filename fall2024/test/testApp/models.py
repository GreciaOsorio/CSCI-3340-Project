from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class UserProfile(models.Model):
    USER_TYPES = [
        ('manager', 'Project Manager'),
        ('teammate', 'Project Teammate')
    ]
    # One user correlates to one user profile.
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE
    )
    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPES
    )
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

class Project(models.Model):
    p_name = models.CharField(max_length=100)
    p_description = models.TextField()
    p_created_date = models.DateTimeField(editable=False)
    p_modified_date = models.DateTimeField()
    p_due_date = models.DateTimeField()
    p_manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_projects'
    )
    # Many users can correlate to many projects.
    p_members = models.ManyToManyField(
        User,
        related_name='assigned_projects'
    )

    def __str__(self):
        return self.p_name

    def get_task_count(self):
        return self.tasks.count()

    def get_completed_task_count(self):
        return self.tasks.filter(status='completed').count()
    
    # Used to properly update the date + time a project is updated.
    def save(self, *args, **kwargs):
        if not self.id:
            self.p_created_date = timezone.now()
        self.p_modified_date = timezone.now()
        return super(Project, self).save(*args, **kwargs)

    # Orders projects in the database based on their due dates (descending order).
    class Meta:
        ordering = ['p_due_date']

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]
    # Identifies what project a task belongs to.
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'    # Used to reference a project's tasks (used in our Project model).
    )
    t_name = models.CharField(max_length=200)
    t_description = models.TextField()
    t_created_date = models.DateTimeField(editable=False)
    t_modified_date = models.DateTimeField()
    t_due_date = models.DateTimeField()
    t_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    t_manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )
    # Many users can be assigned to many tasks.
    t_assignees = models.ManyToManyField(
        User,
        related_name='assigned_tasks',
        blank=True  # This allows the field to be empty.
    )

    def is_unassigned(self):
        return self.t_assignees.count() == 0

    def __str__(self):
        status = " (Unassigned)" if self.is_unassigned() else ""
        return f"{self.project.p_name} - {self.t_name}{status}"
    
    # Used to properly update the date + time a task is updated.
    def save(self, *args, **kwargs):
        if not self.id:
            self.t_created_date = timezone.now()
        self.t_modified_date = timezone.now()
        return super(Task, self).save(*args, **kwargs)

    # Orders tasks in the database based on their due dates (descending order).
    class Meta:
        ordering = ['t_due_date']