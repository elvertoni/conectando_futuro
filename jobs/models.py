from django.db import models
from django.utils import timezone


class JobQuerySet(models.QuerySet):
    def active(self):
        today = timezone.localdate()
        return self.filter(is_active=True).filter(
            models.Q(expires_at__isnull=True) | models.Q(expires_at__gt=today)
        )


class JobManager(models.Manager):
    def get_queryset(self):
        return JobQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('estagio', 'Estágio'),
        ('aprendiz', 'Jovem Aprendiz'),
        ('primeiro_emprego', 'Primeiro Emprego'),
    ]
    SOURCE_CHOICES = [
        ('manual', 'Manual'),
        ('automatico', 'Automático'),
    ]

    title = models.CharField('título', max_length=150)
    company = models.CharField('empresa', max_length=100)
    description = models.TextField('descrição')
    job_type = models.CharField('tipo de vaga', max_length=20, choices=JOB_TYPE_CHOICES)
    area = models.CharField('área de atuação', max_length=100)
    city = models.CharField('cidade', max_length=100)
    state = models.CharField('estado', max_length=2, default='PR')
    external_link = models.URLField('link externo/candidatura')
    source = models.CharField('origem', max_length=20, choices=SOURCE_CHOICES, default='manual')
    is_active = models.BooleanField('ativo', default=True)
    expires_at = models.DateField('expira em', null=True, blank=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    objects = JobManager()

    class Meta:
        verbose_name = 'vaga'
        verbose_name_plural = 'vagas'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.company}"

    @property
    def is_expired(self):
        if self.expires_at:
            return self.expires_at <= timezone.localdate()
        return False
