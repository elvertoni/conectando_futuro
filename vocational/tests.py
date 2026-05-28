from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Question, QuestionOption, VocationalProfile
from .services import local_fallback_analysis

User = get_user_model()

class VocationalModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='aluno@email.com',
            password='password123',
            full_name='Aluno Teste'
        )
        self.question = Question.objects.create(text='Qual seu hobbie?', order=1)
        self.option1 = QuestionOption.objects.create(
            question=self.question,
            text='Programar',
            value='Tecnologia',
            order=1
        )
        self.option2 = QuestionOption.objects.create(
            question=self.question,
            text='Vender',
            value='Vendas',
            order=2
        )

    def test_model_creation(self):
        self.assertEqual(str(self.question), "1. Qual seu hobbie?")
        self.assertEqual(str(self.option1), "1.1 - Programar (Tecnologia)")
        
    def test_vocational_profile_creation(self):
        profile = VocationalProfile.objects.create(user=self.user)
        self.assertEqual(str(profile), f"Perfil de {self.user.email}")
        self.assertEqual(profile.answers, {})

class VocationalServicesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='aluno2@email.com',
            password='password123',
            full_name='Aluno Teste 2'
        )
        self.q1 = Question.objects.create(text='Q1', order=1)
        self.q2 = Question.objects.create(text='Q2', order=2)
        self.q3 = Question.objects.create(text='Q3', order=3)
        
        self.opt1 = QuestionOption.objects.create(question=self.q1, text='Opt1', value='Tecnologia', order=1)
        self.opt2 = QuestionOption.objects.create(question=self.q2, text='Opt2', value='Tecnologia', order=1)
        self.opt3 = QuestionOption.objects.create(question=self.q3, text='Opt3', value='Administração', order=1)

    def test_local_fallback_analysis_calculation(self):
        profile = VocationalProfile.objects.create(user=self.user)
        profile.answers = {
            str(self.q1.id): self.opt1.id,
            str(self.q2.id): self.opt2.id,
            str(self.q3.id): self.opt3.id
        }
        profile.save()
        
        success = local_fallback_analysis(profile)
        self.assertTrue(success)
        
        profile.refresh_from_db()
        self.assertIn('Tecnologia', profile.suggested_areas)
        self.assertIn('Administração', profile.suggested_areas)
        self.assertIn('estagio', profile.recommended_job_types)
        self.assertTrue(len(profile.profile_summary) > 0)
        self.assertTrue(len(profile.strengths) > 0)
        self.assertTrue(len(profile.next_steps) > 0)

class VocationalViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='aluno3@email.com',
            password='password123',
            full_name='Aluno Teste 3'
        )
        self.q1 = Question.objects.create(text='Q1', order=1)
        self.opt1 = QuestionOption.objects.create(question=self.q1, text='Opt1', value='Tecnologia', order=1)

    def test_views_require_authentication(self):
        response = self.client.get(reverse('vocational:questionnaire'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('vocational:result'))
        self.assertEqual(response.status_code, 302)

    def test_questionnaire_view_authenticated(self):
        self.client.login(email='aluno3@email.com', password='password123')
        response = self.client.get(reverse('vocational:questionnaire'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vocational/questionnaire.html')
        self.assertIn('questions', response.context)

    def test_submit_answers_ajax(self):
        self.client.login(email='aluno3@email.com', password='password123')
        payload = {
            'answers': {
                str(self.q1.id): self.opt1.id
            }
        }
        import json
        response = self.client.post(
            reverse('vocational:submit'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['redirect_url'], '/vocational/resultado/')
        
        profile = VocationalProfile.objects.get(user=self.user)
        self.assertEqual(profile.answers, {str(self.q1.id): self.opt1.id})
        self.assertIn('Tecnologia', profile.suggested_areas)
