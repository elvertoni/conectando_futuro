from django.urls import path

from .views import LoginView, LogoutView, RegisterView

app_name = 'accounts'

urlpatterns = [
    path('cadastro/', RegisterView.as_view(), name='register'),
    path('entrar/', LoginView.as_view(), name='login'),
    path('sair/', LogoutView.as_view(), name='logout'),
]
