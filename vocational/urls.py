from django.urls import path
from .views import QuestionnaireView, SubmitAnswersView, VocationalResultView

app_name = 'vocational'

urlpatterns = [
    path('', QuestionnaireView.as_view(), name='questionnaire'),
    path('responder/', SubmitAnswersView.as_view(), name='submit'),
    path('resultado/', VocationalResultView.as_view(), name='result'),
]
