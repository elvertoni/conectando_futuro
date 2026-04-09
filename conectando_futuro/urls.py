from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('', include('accounts.urls', namespace='accounts')),
    path('vagas/', include('jobs.urls', namespace='jobs')),
    path('vocacional/', include('vocational.urls', namespace='vocational')),
    path('curriculo/', include('resume.urls', namespace='resume')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
