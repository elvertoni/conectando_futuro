from django.urls import path
from .views import ResumeWizardView, ResumeSubmitView, ResumeDownloadView

app_name = 'resume'

urlpatterns = [
    path('', ResumeWizardView.as_view(), name='wizard'),
    path('salvar/', ResumeSubmitView.as_view(), name='submit'),
    path('download/', ResumeDownloadView.as_view(), name='download'),
]
