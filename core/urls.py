from django.urls import path
from .views import DesignDraftView

app_name = 'core'

urlpatterns = [
    path('design/', DesignDraftView.as_view(), name='design-draft'),
]
