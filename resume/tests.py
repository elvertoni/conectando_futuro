from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Resume, Education, WorkExperience
from .forms import EducationForm, WorkExperienceForm
import json

User = get_user_model()

class ResumeModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='candidato@email.com',
            password='password123',
            full_name='Candidato Teste'
        )
        
    def test_resume_creation_and_str(self):
        resume = Resume.objects.create(
            user=self.user,
            professional_objective='Estágio na área de desenvolvimento.'
        )
        self.assertEqual(str(resume), f"Currículo de {self.user.email} (v1)")
        
        education = Education.objects.create(
            resume=resume,
            institution='UFPR',
            course='Análise de Sistemas',
            level='superior',
            status='cursando',
            start_year=2023
        )
        self.assertEqual(str(education), "Análise de Sistemas — UFPR")
        
        experience = WorkExperience.objects.create(
            resume=resume,
            role='Auxiliar',
            company='SoftLtda',
            description='Suporte geral',
            start_date='2024-01-01'
        )
        self.assertEqual(str(experience), "Auxiliar na SoftLtda")

class ResumeFormsTestCase(TestCase):
    def test_education_form_validation(self):
        # Missing end_year when status is concluido
        form = EducationForm(data={
            'institution': 'Escola X',
            'course': 'Ensino Médio',
            'level': 'medio',
            'status': 'concluido',
            'start_year': 2020,
            'end_year': None
        })
        self.assertFalse(form.is_valid())
        self.assertIn('end_year', form.errors)

        # end_year before start_year
        form = EducationForm(data={
            'institution': 'Escola X',
            'course': 'Ensino Médio',
            'level': 'medio',
            'status': 'concluido',
            'start_year': 2020,
            'end_year': 2019
        })
        self.assertFalse(form.is_valid())
        self.assertIn('end_year', form.errors)

        # Valid form
        form = EducationForm(data={
            'institution': 'Escola X',
            'course': 'Ensino Médio',
            'level': 'medio',
            'status': 'concluido',
            'start_year': 2020,
            'end_year': 2023
        })
        self.assertTrue(form.is_valid())

    def test_work_experience_form_validation(self):
        # end_date before start_date
        form = WorkExperienceForm(data={
            'role': 'Estagiário',
            'company': 'Empresa Y',
            'description': 'Suporte',
            'start_date': '2024-05-01',
            'end_date': '2024-04-01'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('end_date', form.errors)

class ResumeViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='candidato2@email.com',
            password='password123',
            full_name='Candidato Teste 2'
        )

    def test_views_require_login(self):
        response = self.client.get(reverse('resume:wizard'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('resume:download'))
        self.assertEqual(response.status_code, 302)

    def test_submit_resume_ajax_valid(self):
        self.client.login(email='candidato2@email.com', password='password123')
        
        payload = {
            'objective': 'Jovem Aprendiz administrativo.',
            'skills': ['Excel', 'Comunicação'],
            'languages': [{'language': 'Inglês', 'level': 'Básico'}],
            'education': [
                {
                    'institution': 'Colégio Estadual',
                    'course': 'Ensino Médio',
                    'level': 'medio',
                    'status': 'cursando',
                    'start_year': '2023',
                    'end_year': ''
                }
            ],
            'experience': []
        }
        
        response = self.client.post(
            reverse('resume:submit'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['redirect_url'], '/curriculo/download/')
        
        resume = Resume.objects.get(user=self.user)
        self.assertEqual(resume.professional_objective, 'Jovem Aprendiz administrativo.')
        self.assertEqual(resume.skills, ['Excel', 'Comunicação'])
        self.assertEqual(resume.languages, [{'language': 'Inglês', 'level': 'Básico'}])
        self.assertEqual(resume.education.count(), 1)
