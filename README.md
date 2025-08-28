# RAG FAQ Plurelo

Sistema de perguntas e respostas baseado em Retrieval-Augmented Generation (RAG) desenvolvido com FastAPI.

## 📋 Descrição

O RAG FAQ Plurelo é uma API moderna desenvolvida em Python utilizando FastAPI para fornecer respostas inteligentes baseadas em Retrieval-Augmented Generation. Este projeto foi construído seguindo as melhores práticas de desenvolvimento e oferece uma interface REST para interação.

## 🚀 Tecnologias Utilizadas

- **Python 3.13+**
- **FastAPI** - Framework web moderno e rápido
- **Uvicorn** - Servidor ASGI para aplicações Python
- **Docker** - Containerização da aplicação
- **UV** - Gerenciador de pacotes Python ultra-rápido

## 📦 Instalação e Configuração

### Usando Docker (Recomendado)

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd rag-faq-plurelo
```

2. **Execute com Docker Compose:**
```bash
docker-compose up --build
```

Isso irá construir a imagem do Docker, instalar as dependências e iniciar o servidor da aplicação. A API estará acessível em http://localhost:8000.

### Ambiente Local

Se preferir executar o projeto localmente sem o Docker, siga estas etapas:

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd rag-faq-plurelo
```

2. **Crie um ambiente virtual e instale as dependências:**

É recomendado usar o `uv` para criar um ambiente virtual e instalar as dependências a partir do `pyproject.toml`:

```bash
uv venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
uv sync
```

3. **Inicie o servidor:**

Depois que as dependências estiverem instaladas, você pode iniciar o servidor de desenvolvimento com o Uvicorn:

```bash
uvicorn main:app --reload
```

A API estará acessível em http://localhost:8000.

## 📚 Endpoints da API

A seguir estão os endpoints disponíveis e como interagir com eles.

### Raiz: `GET /`
Retorna uma mensagem básica para indicar que a API está em execução.

**Exemplo de chamada com cURL:**
```bash
curl -X GET "http://localhost:8000/"
```

**Exemplo de resposta:**
```json
{
  "status": "success",
  "message": "API is running",
  "version": "0.1.0"
}
```

### Verificação de Saúde: `GET /health`
Fornece um endpoint de verificação de saúde para monitoramento.

**Exemplo de chamada com cURL:**
```bash
curl -X GET "http://localhost:8000/health"
```

**Exemplo de resposta:**
```json
{
  "status": "success",
  "message": "Health check successful",
  "version": "0.1.0"
}
```

## 📖 Documentação da API

A documentação interativa da API está disponível quando a aplicação está em execução:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🛠️ Desenvolvimento

### Estrutura do Projeto

```
rag-faq-plurelo/
├── main.py              # Arquivo principal da aplicação
├── pyproject.toml       # Configuração do projeto e dependências
├── docker-compose.yml   # Configuração do Docker Compose
├── Dockerfile           # Configuração do container Docker
├── README.md           # Documentação do projeto
└── uv.lock             # Lock file das dependências
```

### Configurações de Desenvolvimento

O projeto utiliza as seguintes ferramentas para manutenção da qualidade do código:

- **Black** - Formatador de código Python
- **isort** - Organizador de imports
- Configuração de linha com 89 caracteres

Para instalar as dependências de desenvolvimento:

```bash
uv sync --extra dev
```

## 🔧 Variáveis de Ambiente

O projeto utiliza variáveis de ambiente para configuração. Crie um arquivo `.env` na raiz do projeto com as configurações necessárias.

## 📄 Licença

Este projeto está sob a licença [inserir licença aqui].

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor, siga as diretrizes de contribuição do projeto.

## 📞 Suporte

Para suporte e dúvidas, entre em contato através de [inserir contato].