from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Job

User = get_user_model()


class JobModelTest(TestCase):
    def setUp(self):
        self.active_job = Job.objects.create(
            title="Desenvolvedor Django",
            company="Empresa A",
            description="Vaga para desenvolvedor Django",
            job_type="estagio",
            area="Tecnologia",
            city="Curitiba",
            external_link="https://exemplo.com",
            is_active=True,
            expires_at=timezone.localdate() + timedelta(days=10)
        )
        self.expired_job = Job.objects.create(
            title="Estagiário",
            company="Empresa B",
            description="Vaga de estágio",
            job_type="estagio",
            area="Tecnologia",
            city="Londrina",
            external_link="https://exemplo.com",
            is_active=True,
            expires_at=timezone.localdate() - timedelta(days=1)
        )
        self.inactive_job = Job.objects.create(
            title="Aprendiz",
            company="Empresa C",
            description="Vaga de aprendiz",
            job_type="aprendiz",
            area="Administração",
            city="Maringá",
            external_link="https://exemplo.com",
            is_active=False,
        )

    def test_job_string_representation(self):
        self.assertEqual(str(self.active_job), "Desenvolvedor Django — Empresa A")

    def test_is_expired_property(self):
        self.assertFalse(self.active_job.is_expired)
        self.assertTrue(self.expired_job.is_expired)
        # Job without expiration date
        no_expiry_job = Job.objects.create(
            title="Suporte",
            company="Empresa D",
            description="Suporte de redes",
            job_type="primeiro_emprego",
            area="Tecnologia",
            city="Curitiba",
            external_link="https://exemplo.com"
        )
        self.assertFalse(no_expiry_job.is_expired)

    def test_active_manager_filter(self):
        active_jobs = Job.objects.active()
        self.assertEqual(active_jobs.count(), 1)
        self.assertIn(self.active_job, active_jobs)
        self.assertNotIn(self.expired_job, active_jobs)
        self.assertNotIn(self.inactive_job, active_jobs)


class JobViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@email.com",
            full_name="User Teste",
            password="password123"
        )
        self.job1 = Job.objects.create(
            title="Estágio em TI",
            company="SoftPR",
            description="Estágio de suporte",
            job_type="estagio",
            area="Tecnologia",
            city="Curitiba",
            external_link="https://exemplo.com"
        )
        self.job2 = Job.objects.create(
            title="Auxiliar de Vendas",
            company="Magasul",
            description="Auxiliar nas vendas",
            job_type="primeiro_emprego",
            area="Vendas",
            city="Londrina",
            external_link="https://exemplo.com"
        )

    def test_list_view_requires_login(self):
        response = self.client.get(reverse('jobs:list'))
        self.assertEqual(response.status_code, 302)

    def test_list_view_authenticated(self):
        self.client.login(email="test@email.com", password="password123")
        response = self.client.get(reverse('jobs:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Estágio em TI")
        self.assertContains(response, "Auxiliar de Vendas")

    def test_list_view_filters(self):
        self.client.login(email="test@email.com", password="password123")
        
        # Filter by city
        response = self.client.get(reverse('jobs:list'), {'city': 'Curitiba'})
        self.assertEqual(len(response.context['jobs']), 1)
        self.assertEqual(response.context['jobs'][0], self.job1)

        # Filter by job type
        response = self.client.get(reverse('jobs:list'), {'job_type': 'primeiro_emprego'})
        self.assertEqual(len(response.context['jobs']), 1)
        self.assertEqual(response.context['jobs'][0], self.job2)

        # Filter by area
        response = self.client.get(reverse('jobs:list'), {'area': 'Tecnologia'})
        self.assertEqual(len(response.context['jobs']), 1)
        self.assertEqual(response.context['jobs'][0], self.job1)
