# Arquitetura

## Stack

| Camada | Tecnologia | Versão |
|---|---|---|
| Linguagem | Python | 3.12+ |
| Framework web | Django | 5.x |
| ORM / Banco | Django ORM + SQLite (dev) / PostgreSQL (prod) | — |
| Frontend | Django Template Language + TailwindCSS | 3.x |
| Tarefas assíncronas | Celery + Redis | 5.x / 7.x |
| IA Vocacional | OpenRouter API (Claude Haiku) | — |
| Geração PDF | WeasyPrint | 62.x |
| Servidor (prod) | Gunicorn + Nginx | — |
| Admin | Django Admin nativo | — |

---

## Apps Django

```
conectando_futuro/          ← projeto Django (settings, urls, wsgi)
├── core/                   ← landing page, dashboard, mixins
├── accounts/               ← autenticação por e-mail, modelo de usuário
├── jobs/                   ← portal de vagas
├── vocational/             ← questionário + análise de perfil IA
└── resume/                 ← gerador de currículo em PDF
```

---

## Estrutura de Arquivos

```
conectando_futuro/
├── manage.py
├── requirements.txt
├── requirements-dev.txt
├── .env
├── .gitignore
│
├── conectando_futuro/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── core/
│   ├── views.py          ← HomeView, DashboardView
│   └── urls.py
│
├── accounts/
│   ├── models.py         ← User (AbstractBaseUser)
│   ├── managers.py       ← UserManager
│   ├── backends.py       ← EmailBackend
│   ├── forms.py          ← RegisterForm, LoginForm
│   ├── views.py          ← RegisterView, LoginView, LogoutView
│   ├── signals.py
│   └── urls.py
│
├── jobs/
│   ├── models.py         ← Job
│   ├── views.py          ← JobListView, JobDetailView
│   ├── admin.py
│   └── urls.py
│
├── vocational/
│   ├── models.py         ← Question, QuestionOption, VocationalProfile
│   ├── views.py          ← QuestionnaireView, SubmitAnswersView, VocationalResultView
│   ├── services.py       ← analyze_profile()
│   ├── admin.py
│   └── urls.py
│
├── resume/
│   ├── models.py         ← Resume, Education, WorkExperience
│   ├── forms.py          ← ResumeForm, EducationForm, WorkExperienceForm
│   ├── views.py          ← ResumeWizardView, ResumeSubmitView, ResumeDownloadView
│   ├── services.py       ← generate_pdf()
│   ├── admin.py
│   └── urls.py
│
├── templates/
│   ├── base.html
│   ├── partials/
│   │   ├── navbar.html
│   │   ├── footer.html
│   │   └── messages.html
│   ├── core/
│   │   ├── home.html
│   │   └── dashboard.html
│   ├── accounts/
│   │   ├── login.html
│   │   └── register.html
│   ├── jobs/
│   │   ├── job_list.html
│   │   └── job_detail.html
│   ├── vocational/
│   │   ├── questionnaire.html
│   │   └── result.html
│   └── resume/
│       ├── resume_form.html
│       ├── resume_download.html
│       └── pdf_template.html
│
└── media/
    └── curriculos/
```

---

## Rotas por App

| App | Rota |
|---|---|
| core | `/` e `/dashboard/` |
| accounts | `/cadastro/`, `/entrar/`, `/sair/` |
| jobs | `/vagas/`, `/vagas/<int:pk>/` |
| vocational | `/vocacional/`, `/vocacional/responder/`, `/vocacional/resultado/` |
| resume | `/curriculo/`, `/curriculo/salvar/`, `/curriculo/download/` |
