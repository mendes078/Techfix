# TechFix — Sistema de Gerenciamento para Assistência Técnica

## Sobre o projeto

O **TechFix** é um sistema desktop desenvolvido como projeto universitário, com o objetivo de auxiliar no gerenciamento das atividades de uma assistência técnica de aparelhos eletrônicos.

A aplicação foi desenvolvida para centralizar informações sobre clientes, aparelhos e ordens de serviço, oferecendo uma maneira mais organizada de acompanhar os atendimentos e consultar indicadores importantes do estabelecimento.

O projeto também teve como propósito aplicar, na prática, conhecimentos de programação, desenvolvimento web, integração com banco de dados e criação de aplicações desktop.

## Objetivos

- Desenvolver um sistema para organizar as operações de uma assistência técnica.
- Facilitar o cadastro e o gerenciamento de clientes e aparelhos.
- Permitir o acompanhamento de ordens de serviço.
- Centralizar informações em um banco de dados local.
- Apresentar indicadores que auxiliem na visualização da situação do estabelecimento.
- Aplicar conceitos de desenvolvimento de software e integração entre diferentes tecnologias.

## Funcionalidades

### Dashboard
- Visualização da quantidade total de clientes cadastrados.
- Visualização da quantidade de aparelhos registrados.
- Acompanhamento do total de ordens de serviço.
- Consulta da receita referente aos serviços concluídos ou entregues.

### Gerenciamento de clientes
- Cadastro de clientes.
- Consulta dos clientes registrados.
- Organização das informações dos clientes.

### Gerenciamento de aparelhos
- Cadastro de aparelhos vinculados aos clientes.
- Consulta e gerenciamento dos aparelhos registrados.

### Gerenciamento de ordens de serviço
- Criação de ordens de serviço.
- Consulta e acompanhamento dos serviços.
- Atualização das informações e dos status das ordens.

## Tecnologias utilizadas

| Tecnologia | Aplicação no projeto |
|---|---|
| Python | Linguagem principal de programação |
| Flask | Desenvolvimento da aplicação e gerenciamento das rotas |
| SQLite | Armazenamento local dos dados |
| HTML5 | Estruturação das páginas |
| CSS3 | Estilização e organização visual |
| JavaScript | Interatividade das interfaces |
| Jinja2 | Renderização dinâmica dos templates |
| PyWebView | Execução da aplicação em uma janela desktop |
| PyInstaller | Empacotamento da aplicação em executável |
| Inno Setup | Criação do instalador para Windows |

## Estrutura do projeto

```text
TechFix/
│
├── app.py
├── desktop.py
├── techfix.db
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   └── ...
│
├── static/
│   ├── style.css
│   ├── script.js
│   └── ...
│
└── README.md
```

## Como executar o projeto

### 1. Pré-requisitos

Para executar o projeto em ambiente de desenvolvimento, é necessário ter:

- Python instalado.
- Git (opcional, para clonar o repositório).

### 2. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
```

Acesse a pasta do projeto:

```bash
cd TechFix
```

### 3. Instalar as dependências

```bash
python -m pip install flask pywebview
```

### 4. Executar a aplicação

```bash
python desktop.py
```

Após a execução, o sistema será aberto em uma janela desktop.

## Distribuição

O TechFix também foi preparado para funcionar como uma aplicação independente no Windows.

Para isso, foram utilizadas as seguintes ferramentas:

- **PyInstaller:** responsável por empacotar a aplicação e suas dependências em uma estrutura executável.
- **Inno Setup:** utilizado para criar um instalador, permitindo a instalação do TechFix no computador e a criação de atalhos para acesso ao programa.

Dessa forma, o usuário pode utilizar o sistema sem precisar executar manualmente os arquivos Python.

## Banco de dados

O projeto utiliza o **SQLite** para armazenar as informações localmente.

O banco de dados é responsável por manter os registros de clientes, aparelhos e ordens de serviço, permitindo que as informações permaneçam disponíveis entre diferentes execuções do programa.

## Aprendizados e conhecimentos aplicados

Durante o desenvolvimento do TechFix, foram trabalhados conceitos importantes para a formação em Ciência da Computação, como:

- Lógica de programação e organização de código.
- Desenvolvimento de aplicações com Python e Flask.
- Integração entre aplicação e banco de dados relacional.
- Operações CRUD (Create, Read, Update e Delete).
- Desenvolvimento de interfaces utilizando HTML, CSS e JavaScript.
- Utilização de templates dinâmicos com Jinja2.
- Estruturação e organização de projetos.
- Empacotamento e distribuição de aplicações desktop.

## Considerações finais

O TechFix representa a aplicação prática de conhecimentos adquiridos ao longo da formação acadêmica, reunindo diferentes tecnologias em uma solução voltada para uma necessidade real: a organização dos processos de uma assistência técnica.

Além de consolidar conceitos de desenvolvimento de software, o projeto proporcionou experiência com integração de tecnologias, persistência de dados e distribuição de aplicações para usuários finais.

---

**Projeto desenvolvido para fins acadêmicos.**
