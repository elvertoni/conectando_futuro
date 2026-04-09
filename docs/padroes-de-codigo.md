# Padrões de Código

Convenções obrigatórias para todo o código do projeto.

---

## Python

| Regra | Detalhe |
|---|---|
| **PEP8** | Todo código Python segue PEP8 |
| **Aspas simples** | Usar `'...'` em vez de `"..."` |
| **Inglês no código** | Variáveis, funções, classes e arquivos em inglês |
| **Português na interface** | Todo texto visível ao usuário em pt-BR |

---

## Django

| Regra | Detalhe |
|---|---|
| **Class Based Views** | Preferência absoluta por CBVs nativas do Django |
| **Apps por domínio** | Cada entidade do sistema em sua própria app Django |
| **`created_at` / `updated_at`** | Todo model deve ter esses dois campos |
| **Signals isolados** | Signals em `signals.py` dentro da app correspondente |
| **Autenticação por e-mail** | `USERNAME_FIELD = 'email'`; sem username padrão |
| **`AUTH_USER_MODEL`** | Sempre `'accounts.User'` |
| **`AUTHENTICATION_BACKENDS`** | `['accounts.backends.EmailBackend']` |

---

## Simplicidade

> Nenhuma funcionalidade além do especificado no PRD deve ser implementada.

- Sem SPA, sem Vue, sem React
- Frontend exclusivamente via Django Template Language + TailwindCSS
- JavaScript puro quando necessário (sem frameworks JS externos)

---

## Performance

| Requisito | Meta |
|---|---|
| Resposta da API | < 500ms |
| Geração de PDF | < 10s |

---

## Settings

Separar em três arquivos:

```
conectando_futuro/settings/
├── base.py         ← configurações comuns
├── development.py  ← DEBUG=True, SQLite
└── production.py   ← DEBUG=False, PostgreSQL via DATABASE_URL
```

Usar `python-decouple` para variáveis sensíveis via `.env`.

---

## Arquivos sensíveis

O `.gitignore` deve excluir: `.env`, `__pycache__`, `*.pyc`, `db.sqlite3`, `media/`.
