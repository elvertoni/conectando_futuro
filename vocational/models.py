from django.db import models
from django.conf import settings

class Question(models.Model):
    text = models.TextField()
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.order}. {self.text[:50]}"

class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    value = models.CharField(max_length=50)  # E.g. 'tecnologia', 'saude', 'administracao'
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.question.order}.{self.order} - {self.text[:30]} ({self.value})"

class VocationalProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vocational_profile')
    answers = models.JSONField(default=dict, blank=True)
    profile_summary = models.TextField(blank=True)
    suggested_areas = models.JSONField(default=list, blank=True)
    recommended_job_types = models.JSONField(default=list, blank=True)
    strengths = models.JSONField(default=list, blank=True)
    next_steps = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.user.email}"
