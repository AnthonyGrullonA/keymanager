from django.urls import path
from . import views

app_name = 'vault'

urlpatterns = [
    # Passwords personales
    path('passwords/', views.password_list, name='password_list'),
    path('passwords/create/', views.password_create, name='password_create'),
    path('passwords/<int:pk>/edit/', views.password_update, name='password_update'),
    path('passwords/<int:pk>/delete/', views.password_delete, name='password_delete'),

    # Copia segura desencriptada (no visible, vía JSON)
    path('passwords/<int:pk>/copy/', views.get_decrypted_password, name='password_copy'),

    # Backup personal
    path('passwords/backup/', views.personal_backup, name='password_backup'),

    # Passwords de grupo
    path('groups/<int:group_id>/passwords/', views.group_password_list, name='group_password_list'),
    path('groups/<int:group_id>/passwords/create/', views.group_password_create, name='group_password_create'),

    # Backup por grupo (sólo líder)
    path('groups/<int:group_id>/passwords/backup/', views.group_password_backup, name='group_password_backup'),
    
    
    
    
    
    
    
    
    #URLS programando plantillas html
    
]
