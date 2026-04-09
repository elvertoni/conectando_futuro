# TASKS.md — Conectando Futuro MVP

Referência: [`PRD.md`](./PRD.md) — seção 13 (Lista de Tarefas por Sprint).

---

## Sprint 0 — Setup e Fundação

**Objetivo:** Projeto Django funcionando com estrutura base, design system e autenticação.

### 1.0 Setup do Projeto

- [x] **1.1** Criar ambiente virtual Python (`python -m venv .venv`)
- [x] **1.2** Instalar dependências iniciais (`django`, `pillow`, `python-decouple`, `weasyprint`, `openai`, `celery`, `redis`)
- [x] **1.3** Criar projeto Django: `django-admin startproject conectando_futuro .`
- [x] **1.4** Configurar `settings.py` para usar `python-decouple` com arquivo `.env`
- [x] **1.5** Criar arquivo `.env` com `SECRET_KEY`, `DEBUG=True`, `ALLOWED_HOSTS`
- [x] **1.6** Criar arquivo `.gitignore` excluindo `.env`, `__pycache__`, `*.pyc`, `db.sqlite3`, `media/`
- [x] **1.7** Criar repositório Git e fazer commit inicial

### 2.0 Estrutura de Apps

- [x] **2.1** Criar app `core`: `python manage.py startapp core`
- [x] **2.2** Criar app `accounts`: `python manage.py startapp accounts`
- [x] **2.3** Criar app `jobs`: `python manage.py startapp jobs`
- [x] **2.4** Criar app `vocational`: `python manage.py startapp vocational`
- [x] **2.5** Criar app `resume`: `python manage.py startapp resume`
- [x] **2.6** Registrar todas as apps em `INSTALLED_APPS` no `settings.py`
- [x] **2.7** Criar arquivo `urls.py` em cada app
- [x] **2.8** Incluir as urls das apps no `urls.py` principal com `include()`

### 3.0 Estrutura de Templates

- [ ] **3.1** Criar pasta `templates/` na raiz do projeto
- [ ] **3.2** Configurar `TEMPLATES['DIRS']` no `settings.py` para apontar para `templates/`
- [ ] **3.3** Criar `templates/base.html` com estrutura HTML5 completa
- [ ] **3.4** Criar `templates/partials/navbar.html` com navbar escura e logo
- [ ] **3.5** Criar `templates/partials/footer.html` com footer simples
- [ ] **3.6** Criar `templates/partials/messages.html` com renderização das mensagens Django
- [ ] **3.7** Criar subpastas: `templates/core/`, `templates/accounts/`, `templates/jobs/`, `templates/vocational/`, `templates/resume/`

### 4.0 Design System Base

- [ ] **4.1** Configurar TailwindCSS via CDN no `base.html` com bloco `extra_head`
- [ ] **4.2** Definir `tailwind.config` inline com fonte Inter e cores customizadas
- [ ] **4.3** Adicionar link do Google Fonts (Inter) no `base.html`
- [ ] **4.4** Criar `templates/partials/button_primary.html` com include reutilizável
- [ ] **4.5** Testar design system criando uma página de rascunho com todos os componentes

---

## Sprint 1 — Autenticação e Site Público

**Objetivo:** Landing page pública + cadastro + login por e-mail + dashboard básico.

### 5.0 Model de Usuário Customizado

- [ ] **5.1** Em `accounts/models.py`, criar `User(AbstractBaseUser, PermissionsMixin)` com campos: `email`, `full_name`, `birth_date`, `city`, `state`, `is_active`, `is_staff`, `created_at`, `updated_at`
- [ ] **5.2** Criar `UserManager(BaseUserManager)` com métodos `create_user()` e `create_superuser()` usando `email` como campo de identificação
- [ ] **5.3** Definir `USERNAME_FIELD = 'email'` e `REQUIRED_FIELDS = ['full_name']` no model
- [ ] **5.4** No `settings.py`, definir `AUTH_USER_MODEL = 'accounts.User'`
- [ ] **5.5** Gerar e aplicar migrations: `python manage.py makemigrations accounts && python manage.py migrate`
- [ ] **5.6** Criar superuser de teste: `python manage.py createsuperuser`

### 6.0 Autenticação — Backend

- [ ] **6.1** Em `accounts/forms.py`, criar `RegisterForm(forms.ModelForm)` com campos: `full_name`, `email`, `birth_date`, `password1`, `password2`
- [ ] **6.2** Em `accounts/forms.py`, criar `LoginForm(forms.Form)` com campos: `email`, `password`
- [ ] **6.3** Em `accounts/views.py`, criar `RegisterView(FormView)` que cria o usuário, faz login automático e redireciona para dashboard
- [ ] **6.4** Em `accounts/views.py`, criar `LoginView(FormView)` que autentica via `authenticate(email=..., password=...)` e redireciona para dashboard
- [ ] **6.5** Em `accounts/views.py`, criar `LogoutView(View)` que chama `logout(request)` e redireciona para home
- [ ] **6.6** Em `accounts/urls.py`, registrar rotas: `/cadastro/`, `/entrar/`, `/sair/`
- [ ] **6.7** Criar `accounts/backends.py` com `EmailBackend(ModelBackend)` que autentica por e-mail
- [ ] **6.8** No `settings.py`, definir `AUTHENTICATION_BACKENDS = ['accounts.backends.EmailBackend']`

### 7.0 Autenticação — Templates

- [ ] **7.1** Criar `templates/accounts/register.html` com formulário de cadastro seguindo design system
- [ ] **7.2** Criar `templates/accounts/login.html` com formulário de login seguindo design system
- [ ] **7.3** Adicionar validação visual de erros por campo nos dois formulários
- [ ] **7.4** Adicionar link "Já tem conta? Entrar" no cadastro e "Não tem conta? Cadastre-se" no login
- [ ] **7.5** Testar fluxo completo: cadastro → login → logout

### 8.0 Site Público — Landing Page

- [ ] **8.1** Em `core/views.py`, criar `HomeView(TemplateView)` com `template_name = 'core/home.html'`
- [ ] **8.2** Em `core/urls.py`, registrar rota `/` para `HomeView`
- [ ] **8.3** Criar `templates/core/home.html` herdando de `base.html`
- [ ] **8.4** Implementar seção **Hero**: título com gradiente, subtítulo, botões "Cadastre-se" e "Entrar", background `from-violet-900 via-slate-900 to-indigo-900`
- [ ] **8.5** Implementar seção **Como Funciona**: 3 cards com ícones e descrição dos módulos
- [ ] **8.6** Implementar seção **Por que usar**: lista de benefícios com ícones check
- [ ] **8.7** Implementar seção **CTA Final**: fundo gradiente com botão de cadastro
- [ ] **8.8** Navbar pública com logo e botões "Entrar" / "Cadastre-se"
- [ ] **8.9** Redirecionar usuários já autenticados de `/` para `/dashboard/`

### 9.0 Dashboard Principal

- [ ] **9.1** Usar `LoginRequiredMixin` nativo do Django em todas as views autenticadas
- [ ] **9.2** Em `core/views.py`, criar `DashboardView(LoginRequiredMixin, TemplateView)` com `template_name = 'core/dashboard.html'`
- [ ] **9.3** Em `core/urls.py`, registrar rota `/dashboard/`
- [ ] **9.4** Criar `templates/core/dashboard.html` com navbar autenticada
- [ ] **9.5** Implementar 3 cards de acesso rápido: Vagas, Vocacional, Currículo — com ícone, título, descrição e botão
- [ ] **9.6** Implementar card de boas-vindas com nome do usuário
- [ ] **9.7** Atualizar `navbar.html` para exibir versão autenticada (nome + logout) quando `user.is_authenticated`

---

## Sprint 2 — Portal de Vagas

**Objetivo:** Listagem, filtro e detalhe de vagas funcionando.

### 10.0 Model de Vagas

- [ ] **10.1** Em `jobs/models.py`, criar `Job(models.Model)` com campos: `title`, `company`, `description`, `job_type` (choices: estagio/aprendiz/primeiro_emprego), `area`, `city`, `state`, `external_link`, `source` (choices: manual/automatico), `is_active`, `expires_at`, `created_at`, `updated_at`
- [ ] **10.2** Adicionar método `__str__` retornando `f'{self.title} — {self.company}'`
- [ ] **10.3** Adicionar propriedade `is_expired` verificando se `expires_at` é passado
- [ ] **10.4** Adicionar Manager customizado `Job.objects.active()` filtrando `is_active=True` e `expires_at > hoje`
- [ ] **10.5** Gerar e aplicar migrations: `python manage.py makemigrations jobs && python manage.py migrate`
- [ ] **10.6** Registrar model no `jobs/admin.py` com `list_display`, `list_filter` e `search_fields`
- [ ] **10.7** Popular banco com 15–20 vagas de teste via fixtures ou pelo Django Admin

### 11.0 Views de Vagas

- [ ] **11.1** Em `jobs/views.py`, criar `JobListView(LoginRequiredMixin, ListView)` com `model = Job`, `template_name = 'jobs/job_list.html'`, `paginate_by = 12`
- [ ] **11.2** Sobrescrever `get_queryset()` para aplicar filtros via `request.GET`: `city`, `job_type`, `area`
- [ ] **11.3** Sobrescrever `get_context_data()` para passar filtros ativos ao template
- [ ] **11.4** Em `jobs/views.py`, criar `JobDetailView(LoginRequiredMixin, DetailView)` com `model = Job`, `template_name = 'jobs/job_detail.html'`
- [ ] **11.5** Em `jobs/urls.py`, registrar rotas: `/vagas/` e `/vagas/<int:pk>/`

### 12.0 Templates de Vagas

- [ ] **12.1** Criar `templates/jobs/job_list.html` com grid de cards (1/2/3 colunas responsivo)
- [ ] **12.2** Implementar card de vaga com: título, empresa, cidade, badge de tipo, data, botão "Ver detalhes"
- [ ] **12.3** Implementar formulário de filtros: selects de cidade, tipo, área + botão aplicar + botão limpar
- [ ] **12.4** Implementar paginação com botões anterior/próximo e indicador de página
- [ ] **12.5** Implementar estado vazio: mensagem quando não há vagas no filtro
- [ ] **12.6** Criar `templates/jobs/job_detail.html` com layout de detalhe completo
- [ ] **12.7** Exibir no detalhe: título, empresa, tipo (badge), cidade/estado, descrição, botão "Candidatar-se" (`target="_blank"`) e botão "Voltar"
- [ ] **12.8** Adicionar link "Vagas" na navbar autenticada

---

## Sprint 3 — Direcionamento Vocacional

**Objetivo:** Questionário + análise IA + resultado com áreas sugeridas.

### 13.0 Models Vocacional

- [ ] **13.1** Em `vocational/models.py`, criar `Question(models.Model)` com campos: `text`, `order`, `created_at`, `updated_at`
- [ ] **13.2** Criar `QuestionOption(models.Model)` com campos: `question (FK)`, `text`, `value`, `order`, `created_at`, `updated_at`
- [ ] **13.3** Criar `VocationalProfile(models.Model)` com campos: `user (OneToOne)`, `answers (JSONField)`, `profile_summary (TextField)`, `suggested_areas (JSONField)`, `recommended_job_types (JSONField)`, `strengths (JSONField)`, `next_steps (TextField)`, `created_at`, `updated_at`
- [ ] **13.4** Gerar e aplicar migrations
- [ ] **13.5** Registrar models no `vocational/admin.py`
- [ ] **13.6** Popular banco com 10 perguntas vocacionais via fixture ou admin

### 14.0 Views Vocacional

- [ ] **14.1** Em `vocational/views.py`, criar `QuestionnaireView(LoginRequiredMixin, TemplateView)` que carrega todas as perguntas e opções
- [ ] **14.2** Criar `SubmitAnswersView(LoginRequiredMixin, View)` que recebe `POST` com respostas em JSON e salva em `VocationalProfile.answers`
- [ ] **14.3** Criar função `analyze_profile(profile_id)` em `vocational/services.py` que monta o prompt e chama a OpenRouter API
- [ ] **14.4** Implementar parsing da resposta JSON da IA e salvar campos no `VocationalProfile`
- [ ] **14.5** Implementar fallback: se a API falhar, salvar perfil com análise padrão genérica
- [ ] **14.6** Criar `VocationalResultView(LoginRequiredMixin, TemplateView)` que exibe o resultado e vagas filtradas pelas `suggested_areas`
- [ ] **14.7** Em `vocational/urls.py`, registrar rotas: `/vocacional/`, `/vocacional/responder/`, `/vocacional/resultado/`

### 15.0 Templates Vocacional

- [ ] **15.1** Criar `templates/vocational/questionnaire.html` com as 10 perguntas
- [ ] **15.2** Implementar barra de progresso visual ("4 de 10 respondidas")
- [ ] **15.3** Estilizar opções como cards de seleção com estado ativo (borda gradiente quando selecionado)
- [ ] **15.4** Criar `templates/vocational/result.html` com layout de resultado
- [ ] **15.5** Exibir no resultado: resumo do perfil, áreas sugeridas (badges), pontos fortes, próximos passos
- [ ] **15.6** Exibir grid de vagas filtradas pelas áreas sugeridas (máximo 6 cards)
- [ ] **15.7** Botão "Refazer questionário" disponível no resultado
- [ ] **15.8** Adicionar link "Vocacional" na navbar autenticada
- [ ] **15.9** Atualizar dashboard com card de status vocacional: "Perfil gerado" ou "Fazer teste"

---

## Sprint 4 — Gerador de Currículo

**Objetivo:** Formulário guiado + geração de PDF para download.

### 16.0 Models de Currículo

- [ ] **16.1** Em `resume/models.py`, criar `Resume(models.Model)` com campos: `user (OneToOne)`, `professional_objective`, `skills (JSONField, default=list)`, `languages (JSONField, default=list)`, `pdf_file (FileField, nullable)`, `version (IntegerField, default=1)`, `created_at`, `updated_at`
- [ ] **16.2** Criar `Education(models.Model)` com campos: `resume (FK)`, `institution`, `course`, `level` (choices: medio/tecnico/superior), `status` (choices: cursando/concluido), `start_year`, `end_year (nullable)`, `created_at`, `updated_at`
- [ ] **16.3** Criar `WorkExperience(models.Model)` com campos: `resume (FK)`, `role`, `company`, `description`, `start_date`, `end_date (nullable)`, `created_at`, `updated_at`
- [ ] **16.4** Gerar e aplicar migrations
- [ ] **16.5** Registrar models no `resume/admin.py`

### 17.0 Views de Currículo

- [ ] **17.1** Em `resume/forms.py`, criar `ResumeForm(ModelForm)` para campos do `Resume`
- [ ] **17.2** Criar `EducationForm(ModelForm)` para `Education`
- [ ] **17.3** Criar `WorkExperienceForm(ModelForm)` para `WorkExperience`
- [ ] **17.4** Em `resume/views.py`, criar `ResumeWizardView(LoginRequiredMixin, TemplateView)` com formulário completo em seções distintas
- [ ] **17.5** Criar `ResumeSubmitView(LoginRequiredMixin, View)` que processa `POST`, cria/atualiza `Resume`, `Education` e `WorkExperience`, e dispara geração do PDF
- [ ] **17.6** Criar função `generate_pdf(resume_id)` em `resume/services.py` que renderiza template HTML e gera PDF via WeasyPrint
- [ ] **17.7** Salvar PDF em `MEDIA_ROOT/curriculos/{user_id}/curriculo_v{version}.pdf`
- [ ] **17.8** Criar `ResumeDownloadView(LoginRequiredMixin, View)` que retorna o PDF como `FileResponse`
- [ ] **17.9** Em `resume/urls.py`, registrar rotas: `/curriculo/`, `/curriculo/salvar/`, `/curriculo/download/`

### 18.0 Templates de Currículo

- [ ] **18.1** Criar `templates/resume/resume_form.html` com formulário dividido em seções: Dados Pessoais, Objetivo e Formação, Habilidades e Idiomas, Experiências
- [ ] **18.2** Implementar navegação entre seções via JavaScript puro (show/hide de divs)
- [ ] **18.3** Implementar indicador de etapas (step indicator) no topo do formulário
- [ ] **18.4** Adicionar campos dinâmicos para formação e experiências via JS
- [ ] **18.5** Criar botão "Gerar currículo" ao final do formulário
- [ ] **18.6** Criar `templates/resume/resume_download.html` com mensagem de sucesso e botão de download
- [ ] **18.7** Criar `templates/resume/pdf_template.html` — HTML autônomo para o PDF: layout A4, tipografia limpa, fundo branco
- [ ] **18.8** Adicionar link "Currículo" na navbar autenticada
- [ ] **18.9** Atualizar dashboard: card de status do currículo com link de download se já gerado
