from django.db import models
from django.conf import settings

def resume_pdf_path(instance, filename):
    return f'curriculos/{instance.user.id}/curriculo_v{instance.version}.pdf'

class Resume(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resume')
    professional_objective = models.TextField(blank=True)
    skills = models.JSONField(default=list, blank=True)  # E.g. ["Python", "Django", "Excel"]
    languages = models.JSONField(default=list, blank=True)  # E.g. [{"language": "Inglês", "level": "Intermediário"}]
    pdf_file = models.FileField(upload_to=resume_pdf_path, null=True, blank=True)
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Currículo de {self.user.email} (v{self.version})"

class Education(models.Model):
    LEVEL_CHOICES = [
        ('medio', 'Ensino Médio'),
        ('tecnico', 'Ensino Técnico'),
        ('superior', 'Ensino Superior'),
    ]
    STATUS_CHOICES = [
        ('cursando', 'Cursando'),
        ('concluido', 'Concluído'),
    ]

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=150)
    course = models.CharField(max_length=150)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    start_year = models.IntegerField()
    end_year = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_year', '-id']

    def __str__(self):
        return f"{self.course} — {self.institution}"

class WorkExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experience')
    role = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date', '-id']

    def __str__(self):
        return f"{self.role} na {self.company}"
