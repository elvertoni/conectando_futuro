from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Mínimo 8 caracteres',
            'class': 'w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 '
                     'text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 '
                     'focus:ring-teal-500 focus:border-transparent transition-all duration-200 text-sm',
        }),
        min_length=8,
    )
    password2 = forms.CharField(
        label='Confirmar senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repita a senha',
            'class': 'w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 '
                     'text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 '
                     'focus:ring-teal-500 focus:border-transparent transition-all duration-200 text-sm',
        }),
    )

    class Meta:
        model = User
        fields = ['full_name', 'email', 'birth_date']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Seu nome completo',
                'class': 'w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 '
                         'text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 '
                         'focus:ring-teal-500 focus:border-transparent transition-all duration-200 text-sm',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'seuemail@exemplo.com',
                'class': 'w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 '
                         'text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 '
                         'focus:ring-teal-500 focus:border-transparent transition-all duration-200 text-sm',
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 '
                         'text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 '
                         'focus:ring-teal-500 focus:border-transparent transition-all duration-200 text-sm',
            }),
        }
        labels = {
            'full_name': 'Nome completo',
            'email': 'E-mail',
            'birth_date': 'Data de nascimento',
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('As senhas não coincidem.')
        return p2

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'placeholder': 'seuemail@exemplo.com',
            'class': 'w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 '
                     'text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 '
                     'focus:ring-teal-500 focus:border-transparent transition-all duration-200 text-sm',
        }),
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Sua senha',
            'class': 'w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 '
                     'text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 '
                     'focus:ring-teal-500 focus:border-transparent transition-all duration-200 text-sm',
        }),
    )
