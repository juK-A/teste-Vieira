from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from datetime import date

class Responsible(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Activities(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name_activity = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    done = models.BooleanField(default=False)
    responsible = models.ForeignKey(Responsible, on_delete=models.PROTECT, related_name='Atividade')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities_created')
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='deleted_activities')
    due_date = models.DateField(null=True, blank=True, verbose_name='Prazo')
    last_deadline_status_notified = models.CharField(max_length=20, null=True, blank=True, editable=False)

    class Meta:
        ordering  = ['-created_at']
    
    def __str__(self):
        return self.name_activity 

    @property
    def deadline_status(self):
        if self.done or not self.due_date:
            return None
        today = date.today()
        days_diff = (self.due_date - today).days
        if days_diff < 0:
            return "Atrasado"
        elif days_diff <= 1:
            return "Quase Atrasado"
        else:
            return "No Prazo"

    @property
    def deadline_status_class(self):
        status = self.deadline_status
        if status == "Atrasado":
            return "status-late"
        elif status == "Quase Atrasado":
            return "status-due-soon"
        elif status == "No Prazo":
            return "status-on-time"
        return ""

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    discord_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    def __str__(self):
        return f'Perfil de {self.user.username}'

class DiscordLinkToken(models.Model):
    user_discord_id = models.CharField(max_length=100, unique=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Token para Discord ID {self.user_discord_id}"