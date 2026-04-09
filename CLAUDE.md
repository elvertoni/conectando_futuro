# CLAUDE.md — Conectando Futuro

Arquivo de contexto do projeto para assistentes de IA.
Fonte de verdade: [`PRD.md`](./PRD.md). Documentação detalhada em [`docs/`](./docs/README.md).

---

## O que é este projeto

**Conectando Futuro** é uma plataforma web Django de empregabilidade juvenil.
Três módulos em uma jornada integrada: Portal de Vagas → Direcionamento Vocacional → Gerador de Currículo em PDF.

Contexto: **2º Desafio EPT-PR** (escola → mercado de trabalho para jovens de 15–24 anos).

---

## Stack

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.12+ / Django 5.x |
| Frontend | Django Template Language + TailwindCSS 3.x (via CDN) |
| Banco (dev) | SQLite |
| Banco (prod) | PostgreSQL via `DATABASE_URL` |
| IA | OpenRouter API — Claude Haiku |
| PDF | WeasyPrint 62.x |
| Tarefas async | Celery + Redis |
| Servidor prod | Gunicorn + Nginx |

---

## Estrutura de Apps

```
core/         ← landing page, dashboard, mixins
accounts/     ← User customizado (AbstractBaseUser), auth por e-mail
jobs/         ← portal de vagas
vocational/   ← questionário + análise IA
resume/       ← gerador de currículo + PDF
```

Cada app tem seu próprio `urls.py`, `views.py`, `models.py` e `admin.py`.
Signals ficam em `signals.py` dentro da própria app.  
Services (lógica de negócio) ficam em `services.py`.

---

## Regras obrigatórias

### Python / Django

- PEP8 em todo o código Python. Aspas simples.
- **Class Based Views** — preferência absoluta. Sem function-based views.
- **Inglês** em todo o código (variáveis, funções, classes, arquivos).
- **Português** em todo texto visível ao usuário (pt-BR).
- Todo `Model` deve ter `created_at` e `updated_at`.
- `AUTH_USER_MODEL = 'accounts.User'` — nunca usar o User padrão do Django.
- Autenticação via e-mail: `USERNAME_FIELD = 'email'`, `AUTHENTICATION_BACKENDS = ['accounts.backends.EmailBackend']`.
- Sem funcionalidades além do especificado no PRD. Sem SPA, sem React, sem Vue.

### Frontend

- TailwindCSS via CDN com `tailwind.config` inline no `base.html`.
- Fonte: **Inter** (Google Fonts).
- Tema escuro obrigatório: `bg-[#0F0F1A] text-slate-100`.
- JavaScript puro quando necessário — sem frameworks JS externos.
- Responsivo: mobile-first, funcional em 320px+.

---

## Design System (resumo)

| Token | Valor |
|---|---|
| Fundo principal | `#0F0F1A` |
| Fundo card | `#1A1A2E` |
| Gradiente primário | `from-violet-600 via-purple-600 to-indigo-600` |
| Texto principal | `#F1F5F9` |
| Texto secundário | `#94A3B8` |
| Borda sutil | `#1E293B` |
| Sucesso | `#10B981` |
| Erro | `#EF4444` |

Componentes padronizados: ver [`docs/design-system.md`](./docs/design-system.md).

---

## Models principais

| Model | App | Campos-chave |
|---|---|---|
| `User` | accounts | `email` (UK), `full_name`, `birth_date`, `city`, `state` |
| `Job` | jobs | `title`, `company`, `job_type`, `area`, `city`, `is_active`, `expires_at` |
| `Question` / `QuestionOption` | vocational | questionário vocacional |
| `VocationalProfile` | vocational | `user` (1:1), `answers`, `suggested_areas`, `profile_summary` |
| `Resume` | resume | `user` (1:1), `skills`, `languages`, `pdf_file`, `version` |
| `Education` | resume | FK → Resume |
| `WorkExperience` | resume | FK → Resume |

Schema completo: [`docs/modelos.md`](./docs/modelos.md).

---

## Rotas

| URL | View | App |
|---|---|---|
| `/` | `HomeView` | core |
| `/dashboard/` | `DashboardView` | core |
| `/cadastro/` | `RegisterView` | accounts |
| `/entrar/` | `LoginView` | accounts |
| `/sair/` | `LogoutView` | accounts |
| `/vagas/` | `JobListView` | jobs |
| `/vagas/<int:pk>/` | `JobDetailView` | jobs |
| `/vocacional/` | `QuestionnaireView` | vocational |
| `/vocacional/responder/` | `SubmitAnswersView` | vocational |
| `/vocacional/resultado/` | `VocationalResultView` | vocational |
| `/curriculo/` | `ResumeWizardView` | resume |
| `/curriculo/salvar/` | `ResumeSubmitView` | resume |
| `/curriculo/download/` | `ResumeDownloadView` | resume |

---

## Settings

```
conectando_futuro/settings/
├── base.py         ← configurações comuns
├── development.py  ← DEBUG=True, SQLite
└── production.py   ← DEBUG=False, PostgreSQL
```

Variáveis sensíveis via `python-decouple` + `.env`.  
`.gitignore` exclui: `.env`, `__pycache__`, `*.pyc`, `db.sqlite3`, `media/`.

---

## Performance

- Resposta de API < 500ms
- Geração de PDF < 10s
- PDF salvo em `media/curriculos/{user_id}/curriculo_v{version}.pdf`

---

## Documentação

| Arquivo | Conteúdo |
|---|---|
| [`docs/visao-geral.md`](./docs/visao-geral.md) | Produto, propósito, público, objetivos |
| [`docs/arquitetura.md`](./docs/arquitetura.md) | Stack, apps, estrutura de arquivos |
| [`docs/modelos.md`](./docs/modelos.md) | Schema de dados completo |
| [`docs/design-system.md`](./docs/design-system.md) | Cores, tipografia, componentes |
| [`docs/padroes-de-codigo.md`](./docs/padroes-de-codigo.md) | PEP8, CBVs, convenções Django |
| [`docs/funcionalidades.md`](./docs/funcionalidades.md) | Requisitos funcionais e user stories |
