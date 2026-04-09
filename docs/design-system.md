# Design System

## Identidade Visual

Design moderno, escuro e com gradientes vibrantes. A paleta comunica tecnologia, confiança e juventude.

---

## Paleta de Cores

| Uso | Valor |
|---|---|
| Fundo principal | `#0F0F1A` |
| Fundo card/surface | `#1A1A2E` |
| Fundo elevado | `#16213E` |
| Gradiente primário | `from-violet-600 via-purple-600 to-indigo-600` |
| Gradiente accent | `from-cyan-500 to-blue-600` |
| Gradiente hero | `from-violet-900 via-slate-900 to-indigo-900` |
| Texto principal | `#F1F5F9` (slate-100) |
| Texto secundário | `#94A3B8` (slate-400) |
| Texto muted | `#64748B` (slate-500) |
| Borda sutil | `#1E293B` (slate-800) |
| Borda destaque | `#6D28D9` (violet-700) |
| Sucesso | `#10B981` (emerald-500) |
| Erro | `#EF4444` (red-500) |
| Aviso | `#F59E0B` (amber-500) |
| Info | `#3B82F6` (blue-500) |

---

## Tipografia

Fonte: **Inter** (Google Fonts) — pesos: 300, 400, 500, 600, 700, 800.

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
```

| Uso | Classe Tailwind |
|---|---|
| Título hero | `text-4xl md:text-6xl font-extrabold tracking-tight` |
| Título de página | `text-2xl md:text-3xl font-bold` |
| Subtítulo | `text-lg font-semibold text-slate-300` |
| Corpo | `text-sm md:text-base font-normal text-slate-300` |
| Caption / label | `text-xs font-medium text-slate-400 uppercase tracking-wider` |

---

## Base Template

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}Conectando Futuro{% endblock %}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: { sans: ['Inter', 'sans-serif'] }
        }
      }
    }
  </script>
  {% block extra_head %}{% endblock %}
</head>
<body class="bg-[#0F0F1A] text-slate-100 font-sans antialiased min-h-screen">

  {% include 'partials/navbar.html' %}

  <main>
    {% include 'partials/messages.html' %}
    {% block content %}{% endblock %}
  </main>

  {% include 'partials/footer.html' %}

  {% block extra_js %}{% endblock %}
</body>
</html>
```

---

## Componentes

### Botões

```html
<!-- Primário -->
<button class="inline-flex items-center gap-2 px-6 py-3 rounded-xl
               bg-gradient-to-r from-violet-600 to-indigo-600
               hover:from-violet-500 hover:to-indigo-500
               text-white font-semibold text-sm
               shadow-lg shadow-violet-500/25
               transition-all duration-200 focus:outline-none
               focus:ring-2 focus:ring-violet-500 focus:ring-offset-2
               focus:ring-offset-slate-900">
  Entrar
</button>

<!-- Secundário (outline) -->
<button class="inline-flex items-center gap-2 px-6 py-3 rounded-xl
               border border-slate-700 hover:border-violet-500
               text-slate-300 hover:text-white font-semibold text-sm
               bg-transparent hover:bg-slate-800/50
               transition-all duration-200">
  Saiba mais
</button>

<!-- Ghost -->
<button class="inline-flex items-center gap-1 text-violet-400
               hover:text-violet-300 font-medium text-sm
               transition-colors duration-200">
  Ver todas as vagas →
</button>

<!-- Perigo -->
<button class="inline-flex items-center gap-2 px-4 py-2 rounded-lg
               bg-red-500/10 hover:bg-red-500/20 border border-red-500/30
               text-red-400 hover:text-red-300 font-medium text-sm
               transition-all duration-200">
  Excluir
</button>
```

### Inputs e Formulários

```html
<!-- Label -->
<label class="block text-xs font-medium text-slate-400 uppercase tracking-wider mb-1.5">
  E-mail
</label>

<!-- Input -->
<input type="email"
       class="w-full px-4 py-3 rounded-xl
              bg-slate-800/60 border border-slate-700
              text-slate-100 placeholder-slate-500
              focus:outline-none focus:ring-2 focus:ring-violet-500
              focus:border-transparent
              transition-all duration-200 text-sm">

<!-- Select -->
<select class="w-full px-4 py-3 rounded-xl
               bg-slate-800/60 border border-slate-700
               text-slate-100
               focus:outline-none focus:ring-2 focus:ring-violet-500
               focus:border-transparent transition-all duration-200 text-sm">

<!-- Textarea -->
<textarea class="w-full px-4 py-3 rounded-xl
                 bg-slate-800/60 border border-slate-700
                 text-slate-100 placeholder-slate-500
                 focus:outline-none focus:ring-2 focus:ring-violet-500
                 focus:border-transparent resize-none
                 transition-all duration-200 text-sm" rows="4">
</textarea>

<!-- Erro de campo -->
<p class="mt-1.5 text-xs text-red-400 flex items-center gap-1">
  <svg class="w-3 h-3">...</svg>
  Campo obrigatório
</p>
```

### Cards

```html
<!-- Card padrão -->
<div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-6
            hover:border-slate-700 transition-all duration-200
            backdrop-blur-sm">
</div>

<!-- Card com borda gradiente -->
<div class="relative rounded-2xl p-px
            bg-gradient-to-br from-violet-600/30 via-slate-800 to-indigo-600/20">
  <div class="bg-slate-900 rounded-2xl p-6">
    <!-- conteúdo -->
  </div>
</div>

<!-- Card de vaga -->
<div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-5
            hover:border-violet-500/50 hover:shadow-lg hover:shadow-violet-500/10
            transition-all duration-300 cursor-pointer group">
</div>
```

### Badges de Tipo de Vaga

```html
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs
             font-medium bg-violet-500/15 text-violet-300 border border-violet-500/30">
  Estágio
</span>

<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs
             font-medium bg-cyan-500/15 text-cyan-300 border border-cyan-500/30">
  Jovem Aprendiz
</span>

<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs
             font-medium bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
  Primeiro Emprego
</span>
```

### Alertas (mensagens Django)

```html
{% for message in messages %}
<div class="flex items-start gap-3 px-4 py-3 rounded-xl border text-sm
            {% if message.tags == 'success' %}
              bg-emerald-500/10 border-emerald-500/30 text-emerald-300
            {% elif message.tags == 'error' %}
              bg-red-500/10 border-red-500/30 text-red-300
            {% else %}
              bg-blue-500/10 border-blue-500/30 text-blue-300
            {% endif %}">
  {{ message }}
</div>
{% endfor %}
```

### Navbar (autenticada)

```html
<nav class="sticky top-0 z-50 border-b border-slate-800/80
            bg-slate-950/80 backdrop-blur-md">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-16">

      <!-- Logo -->
      <a href="/" class="flex items-center gap-2">
        <span class="text-lg font-bold bg-gradient-to-r from-violet-400
                     to-indigo-400 bg-clip-text text-transparent">
          Conectando Futuro
        </span>
      </a>

      <!-- Links (desktop) -->
      <div class="hidden md:flex items-center gap-1">
        <a href="/vagas/" class="px-4 py-2 rounded-lg text-sm font-medium
                                  text-slate-400 hover:text-slate-100
                                  hover:bg-slate-800 transition-all duration-200">
          Vagas
        </a>
        <!-- ... -->
      </div>

      <!-- Avatar / logout -->
      <div class="flex items-center gap-3">
        <span class="text-sm text-slate-400">Olá, {{ user.first_name }}</span>
        <a href="/sair/" class="px-4 py-2 rounded-lg text-sm font-medium
                                 text-slate-400 hover:text-red-400
                                 hover:bg-red-500/10 transition-all duration-200">
          Sair
        </a>
      </div>

    </div>
  </div>
</nav>
```

### Layout e Grid

```html
<!-- Container principal -->
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

<!-- Grid de vagas (3 colunas) -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">

<!-- Grid de dashboard (2+1) -->
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
  <div class="lg:col-span-2">...</div>
  <div>...</div>
</div>

<!-- Seção com espaçamento -->
<section class="py-16 md:py-24">
```
