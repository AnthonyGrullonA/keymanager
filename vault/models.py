from django.db import models
from django.contrib.auth import get_user_model
#from teams.models import Team  # Asegúrate que la app 'teams' esté creada.

User = get_user_model()

class PasswordGroup(models.Model):
    #team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='password_groups')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Grupo de Contraseñas'
        verbose_name_plural = 'Grupos de Contraseñas'

    #def __str__(self):
        #return f"{self.name} ({self.team.name})"


class Password(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passwords')
    group = models.ForeignKey(PasswordGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='passwords')
    title = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password_encrypted = models.TextField()
    url = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contraseña'
        verbose_name_plural = 'Contraseñas'

    def __str__(self):
        return self.title
