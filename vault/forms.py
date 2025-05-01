from django import forms
from .models import Password
from vault.utils.encryption import get_fernet  # Usamos el helper desde utils

class PasswordForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(),
        help_text='La contraseña será almacenada de forma segura y encriptada.'
    )

    class Meta:
        model = Password
        fields = ['title', 'username', 'password', 'url', 'notes', 'group']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fernet = get_fernet()

        if self.instance and self.instance.pk:
            try:
                # Desencripta el valor almacenado
                decrypted_password = fernet.decrypt(self.instance.password_encrypted.encode()).decode()
                self.fields['password'].initial = decrypted_password
            except Exception as e:
                print(f"[WARN] No se pudo desencriptar la contraseña: {e}")
                self.fields['password'].initial = ''

    def save(self, commit=True):
        instance = super().save(commit=False)
        plain_password = self.cleaned_data.get('password')

        if plain_password:
            fernet = get_fernet()
            instance.password_encrypted = fernet.encrypt(plain_password.encode()).decode()

        if commit:
            instance.save()
        return instance
