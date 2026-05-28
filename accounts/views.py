from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from .forms import LoginForm, RegisterForm


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('core:dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='accounts.backends.EmailBackend')
        messages.success(self.request, 'Cadastro realizado com sucesso! Bem-vindo(a)!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Corrija os erros abaixo para continuar.')
        return super().form_invalid(form)


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('core:dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user, backend='accounts.backends.EmailBackend')
            messages.success(self.request, f'Bem-vindo(a) de volta, {user.full_name}!')
            return super().form_valid(form)
        messages.error(self.request, 'E-mail ou senha inválidos.')
        return self.form_invalid(form)


class LogoutView(View):

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, 'Você saiu da sua conta.')
        return redirect('core:home')
