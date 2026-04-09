# Funcionalidades

Requisitos funcionais e user stories por módulo.

---

## Site Público

- **RF01** — Exibir página inicial pública com apresentação da plataforma
- **RF02** — Disponibilizar botões de "Cadastre-se" e "Entrar" na página pública
- **RF03** — Exibir seções: hero, como funciona, benefícios e chamada para ação

---

## Autenticação

- **RF04** — Permitir cadastro com nome completo, e-mail, senha e data de nascimento
- **RF05** — Autenticar usuário via e-mail (substituindo o username padrão do Django)
- **RF06** — Redirecionar para o dashboard após login bem-sucedido
- **RF07** — Permitir logout do sistema
- **RF08** — Exibir mensagens de erro de autenticação em português

### User Stories

**US01 — Cadastro**
> Como jovem, quero me cadastrar para acessar os recursos da plataforma.

Critérios: formulário com nome, e-mail, senha, confirmação e nascimento; e-mail único; senha ≥ 8 chars; redirecionamento ao dashboard; erros em português.

**US02 — Login por e-mail**
> Como usuário cadastrado, quero fazer login com meu e-mail e senha.

Critérios: login por e-mail (não username); mensagem de erro clara; redirecionamento ao dashboard; sessão com cookie seguro.

**US03 — Logout**
> Como usuário autenticado, quero sair da minha conta.

Critérios: botão de logout na navbar; redirecionamento para página pública; sessão encerrada no servidor.

---

## Portal de Vagas

- **RF12** — Listar vagas com paginação (12 por página)
- **RF13** — Filtrar por cidade, tipo (estágio/aprendiz/primeiro emprego) e área
- **RF14** — Exibir página de detalhe de cada vaga
- **RF15** — Permitir cadastro de vagas pelo admin do Django
- **RF16** — Ocultar automaticamente vagas expiradas

### User Stories

**US04 — Listagem de vagas**
> Como jovem, quero ver as vagas disponíveis.

Critérios: cards com título, empresa, cidade, tipo e data; paginação de 12; apenas vagas ativas; layout responsivo.

**US05 — Filtro de vagas**
> Como jovem, quero filtrar as vagas por cidade, tipo e área.

Critérios: filtros de cidade, tipo e área; contagem de resultados; botão de limpar filtros.

**US06 — Detalhe da vaga**
> Como jovem, quero ver todos os detalhes de uma vaga para decidir se me candidato.

Critérios: título, empresa, descrição completa, cidade, tipo; botão "Candidatar-se" (link externo, nova aba); botão "Voltar".

---

## Direcionamento Vocacional

- **RF17** — Exibir questionário vocacional com 10 perguntas de múltipla escolha
- **RF18** — Salvar respostas e enviar para análise via IA (OpenRouter)
- **RF19** — Exibir resultado com: resumo de perfil, áreas sugeridas e próximos passos
- **RF20** — Mostrar vagas filtradas pelo perfil gerado no resultado

### User Stories

**US07 — Questionário vocacional**
> Como jovem, quero responder um questionário para descobrir meu perfil profissional.

Critérios: 10 perguntas de múltipla escolha; todas obrigatórias antes do envio; feedback visual de progresso ("4 de 10").

**US08 — Resultado vocacional**
> Como jovem, quero ver o resultado da análise com sugestões de áreas profissionais.

Critérios: resumo do perfil, áreas sugeridas, pontos fortes e próximos passos; vagas filtradas pelas áreas; resultado salvo no dashboard; possibilidade de refazer.

---

## Gerador de Currículo

- **RF21** — Exibir formulário multi-step para preenchimento do currículo
- **RF22** — Permitir informar: dados pessoais, objetivo, formação, habilidades, idiomas e experiências
- **RF23** — Gerar PDF do currículo via WeasyPrint
- **RF24** — Disponibilizar link de download do PDF gerado
- **RF25** — Permitir reedição e regeneração do currículo

### User Stories

**US09 — Preenchimento do currículo**
> Como jovem, quero preencher meus dados profissionais para gerar um currículo.

Critérios: formulário em etapas (dados pessoais / objetivo+formação / habilidades+idiomas / experiências); dados salvos a cada etapa; navegação entre steps; campos opcionais indicados.

**US10 — Geração e download do PDF**
> Como jovem, quero gerar meu currículo em PDF para usar nas candidaturas.

Critérios: botão "Gerar currículo" após preenchimento; link de download após geração; possibilidade de reeditar e regenerar; PDF com layout A4 limpo.

---

## Dashboard

- **RF09** — Exibir painel principal após login com resumo dos módulos
- **RF10** — Indicar progresso do usuário (perfil preenchido, currículo gerado, vagas visualizadas)
- **RF11** — Disponibilizar acesso rápido aos três módulos
