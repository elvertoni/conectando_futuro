# Modelos de Dados

## User (accounts)

| Campo | Tipo | Detalhe |
|---|---|---|
| `id` | int PK | — |
| `email` | string UK | Campo de identificação (USERNAME_FIELD) |
| `full_name` | string | — |
| `birth_date` | date | — |
| `city` | string | — |
| `state` | string | — |
| `is_active` | bool | — |
| `is_staff` | bool | — |
| `created_at` | datetime | Auto |
| `updated_at` | datetime | Auto |

- Herda de `AbstractBaseUser` e `PermissionsMixin`
- Gerenciador: `UserManager(BaseUserManager)` com `create_user()` e `create_superuser()`
- Backend de autenticação: `accounts.backends.EmailBackend`

---

## Job (jobs)

| Campo | Tipo | Detalhe |
|---|---|---|
| `id` | int PK | — |
| `title` | string | — |
| `company` | string | — |
| `description` | text | — |
| `job_type` | string choices | `estagio` / `aprendiz` / `primeiro_emprego` |
| `area` | string | — |
| `city` | string | — |
| `state` | string | — |
| `external_link` | string | Link de candidatura |
| `source` | string choices | `manual` / `automatico` |
| `is_active` | bool | — |
| `expires_at` | date | — |
| `created_at` | datetime | Auto |
| `updated_at` | datetime | Auto |

- `__str__` retorna `f'{self.title} — {self.company}'`
- Propriedade `is_expired`: verifica se `expires_at` é passado
- Manager customizado `Job.objects.active()`: filtra `is_active=True` e `expires_at > hoje`

---

## Question e QuestionOption (vocational)

**Question**

| Campo | Tipo |
|---|---|
| `id` | int PK |
| `text` | string |
| `order` | int |
| `created_at` | datetime |
| `updated_at` | datetime |

**QuestionOption**

| Campo | Tipo | Detalhe |
|---|---|---|
| `id` | int PK | — |
| `question` | FK → Question | — |
| `text` | string | Texto exibido |
| `value` | string | Valor usado no prompt da IA |
| `order` | int | — |
| `created_at` | datetime | — |
| `updated_at` | datetime | — |

---

## VocationalProfile (vocational)

| Campo | Tipo |
|---|---|
| `id` | int PK |
| `user` | OneToOne → User |
| `answers` | JSONField |
| `profile_summary` | text |
| `suggested_areas` | JSONField |
| `recommended_job_types` | JSONField |
| `strengths` | JSONField |
| `next_steps` | text |
| `created_at` | datetime |
| `updated_at` | datetime |

---

## Resume, Education e WorkExperience (resume)

**Resume**

| Campo | Tipo | Detalhe |
|---|---|---|
| `id` | int PK | — |
| `user` | OneToOne → User | — |
| `professional_objective` | text | — |
| `skills` | JSONField | `default=list` |
| `languages` | JSONField | `default=list` |
| `pdf_file` | FileField | Nullable; salvo em `media/curriculos/{user_id}/` |
| `version` | int | `default=1` |
| `created_at` | datetime | — |
| `updated_at` | datetime | — |

**Education**

| Campo | Tipo | Detalhe |
|---|---|---|
| `id` | int PK | — |
| `resume` | FK → Resume | — |
| `institution` | string | — |
| `course` | string | — |
| `level` | string choices | `medio` / `tecnico` / `superior` |
| `status` | string choices | `cursando` / `concluido` |
| `start_year` | int | — |
| `end_year` | int | Nullable |
| `created_at` | datetime | — |
| `updated_at` | datetime | — |

**WorkExperience**

| Campo | Tipo | Detalhe |
|---|---|---|
| `id` | int PK | — |
| `resume` | FK → Resume | — |
| `role` | string | — |
| `company` | string | — |
| `description` | text | — |
| `start_date` | date | — |
| `end_date` | date | Nullable |
| `created_at` | datetime | — |
| `updated_at` | datetime | — |

---

## Relacionamentos

```
User  ──(1:1)──  VocationalProfile
User  ──(1:1)──  Resume
Resume  ──(1:N)──  Education
Resume  ──(1:N)──  WorkExperience
```
