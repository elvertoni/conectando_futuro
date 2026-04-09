# Agentes — Conectando Futuro

Agentes especializados para o time de desenvolvimento do projeto.
Cada agente tem um escopo bem definido. Use o agente correto para cada tarefa.

---

## Índice

| Agente | Arquivo | Quando usar |
|---|---|---|
| **Django Backend** | [django-backend.md](./django-backend.md) | Models, views (CBVs), forms, URLs, admin, signals, services, settings |
| **Django Templates** | [django-templates.md](./django-templates.md) | Templates HTML, componentes TailwindCSS, design system, responsividade |
| **QA Engineer** | [qa-engineer.md](./qa-engineer.md) | Testes funcionais, Playwright, verificação de fluxos end-to-end |

---

## Regras gerais

- **MCP context7**: obrigatório nos agentes de código Django para garantir documentação atualizada.
- **MCP playwright**: obrigatório no agente de QA para verificação do sistema via browser.
- Nunca misturar responsabilidades entre agentes.
- Em caso de dúvida sobre qual usar, consulte o escopo abaixo.

---

## Escopos detalhados

### `django-backend`

Use para qualquer trabalho em:
- `models.py` — criação e edição de models Django
- `views.py` — CBVs (ListView, DetailView, FormView, View, etc.)
- `forms.py` — ModelForms e Forms Django
- `urls.py` — roteamento das apps
- `admin.py` — configuração do Django Admin
- `signals.py` — signals isolados por app
- `services.py` — lógica de negócio (analyze_profile, generate_pdf)
- `settings/` — configurações base, dev e produção
- `backends.py` — EmailBackend de autenticação
- Migrations

### `django-templates`

Use para qualquer trabalho em:
- `templates/**/*.html` — todos os templates Django
- `partials/` — navbar, footer, messages
- Componentes do design system (botões, cards, badges, inputs)
- Responsividade e layout TailwindCSS
- JavaScript puro inline nos templates

### `qa-engineer`

Use para:
- Escrever e executar testes com Playwright
- Verificar fluxos end-to-end (cadastro → login → dashboard → módulos)
- Testar formulários, filtros e geração de PDF
- Checar responsividade via browser
- Validar mensagens de erro e redirecionamentos
