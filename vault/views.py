from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
from django.core.files.storage import default_storage
from .models import Password, PasswordGroup
from .forms import PasswordForm
from vault.utils.encryption import get_fernet  # Importación correcta
import json

# -------- VISTAS PERSONALES --------

@login_required
def password_list(request):
    passwords = Password.objects.filter(owner=request.user, group__isnull=True)
    return render(request, 'vault/password_list.html', {'passwords': passwords})

@login_required
def password_create(request):
    form = PasswordForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.owner = request.user
        instance.group = None
        instance.save()
        return redirect('vault:password_list')
    return render(request, 'vault/password_form.html', {'form': form})

@login_required
def password_update(request, pk):
    password = get_object_or_404(Password, pk=pk, owner=request.user, group__isnull=True)
    form = PasswordForm(request.POST or None, instance=password)
    if form.is_valid():
        form.save()
        return redirect('vault:password_list')
    return render(request, 'vault/password_form.html', {'form': form})

@login_required
def password_delete(request, pk):
    password = get_object_or_404(Password, pk=pk, owner=request.user)
    password.delete()
    return redirect('vault:password_list')

# -------- COPIADO SEGURO --------

@login_required
def get_decrypted_password(request, pk):
    password = get_object_or_404(Password, pk=pk)

    # Verifica permisos
    if password.owner != request.user and (not password.group or password.group.team not in request.user.teams.all()):
        return HttpResponseForbidden()

    fernet = get_fernet()
    decrypted = fernet.decrypt(password.password_encrypted.encode()).decode()
    return JsonResponse({'password': decrypted})

# -------- BACKUP PERSONAL --------

@login_required
def personal_backup(request):
    passwords = Password.objects.filter(owner=request.user, group__isnull=True)
    data = [
        {
            'title': p.title,
            'username': p.username,
            'password': p.password_encrypted,
            'url': p.url,
            'notes': p.notes,
        } for p in passwords
    ]
    response = JsonResponse(data, safe=False)
    response['Content-Disposition'] = 'attachment; filename=personal_passwords_backup.json'
    return response

# -------- VISTAS DE GRUPO --------

@login_required
def group_password_list(request, group_id):
    group = get_object_or_404(PasswordGroup, id=group_id)
    if request.user not in group.team.members.all():
        return HttpResponseForbidden()
    passwords = Password.objects.filter(group=group)
    return render(request, 'vault/group_password_list.html', {'group': group, 'passwords': passwords})

@login_required
def group_password_create(request, group_id):
    group = get_object_or_404(PasswordGroup, id=group_id)
    if request.user not in group.team.members.all():
        return HttpResponseForbidden()

    form = PasswordForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.owner = request.user
        instance.group = group
        instance.save()
        return redirect('vault:group_password_list', group_id=group.id)
    return render(request, 'vault/password_form.html', {'form': form, 'group': group})

@login_required
def group_password_backup(request, group_id):
    group = get_object_or_404(PasswordGroup, id=group_id)
    if not request.user == group.team.leader:
        return HttpResponseForbidden()

    passwords = Password.objects.filter(group=group)
    data = [
        {
            'title': p.title,
            'username': p.username,
            'password': p.password_encrypted,
            'url': p.url,
            'notes': p.notes,
        } for p in passwords
    ]
    response = JsonResponse(data, safe=False)
    response['Content-Disposition'] = f'attachment; filename=group_{group.id}_passwords_backup.json'
    return response
