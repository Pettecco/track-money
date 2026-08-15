# Track Money

Aplicação de finanças pessoais desenvolvida como projeto prático do curso **Domain-Driven Design em Python: Da modelagem de domínio à arquitetura de sistemas** da Alura.

Este projeto demonstra a aplicação de conceitos de DDD na construção de um sistema modular, com foco em modelagem de domínio rica e arquitetura orientada ao negócio.

## Sobre o Projeto

O Track Money é um sistema para gerenciamento de finanças pessoais que permite:

- Cadastro e autenticação de usuários
- Gerenciamento de planos de assinatura
- Controle de contas bancárias
- Validação de regras de negócio no domínio

## Conceitos de DDD Aplicados

### Bounded Contexts

O sistema está organizado em três contextos delimitados claros:

- **Authentication**: Gerenciamento de usuários, autenticação e autorização via JWT
- **Subscription**: Controle de planos de assinatura e relacionamento usuário-plano
- **Movement**: Gerenciamento de contas bancárias e movimentações financeiras

Cada contexto possui sua própria entidade User, isolada e com responsabilidades específicas ao seu domínio, evitando acoplamento entre módulos.

### Entidades Ricas

As entidades possuem comportamento e validação de estado, não sendo meros containers de dados:

```python
class User(Base):
    def __init__(self, name: str, email: str, password: str):
        DomainException.validate(
            bool(name) and len(name) <= 128,
            "Name is required and must be at most 128 characters long.",
        )
        self.name = name
        # ... validações e comportamento
```

### Value Objects

O módulo Movement utiliza Value Objects para representar conceitos do domínio sem identidade própria:

```python
class User:
    """Value object representing a user associated with a bank account."""
    name: str
    email: str
```

### Aggregate Roots

A entidade User no módulo Subscription atua como Aggregate Root, gerenciando o ciclo de vida dos planos do usuário:

```python
def add_plan(self, plan: Plan, credit_card: str | None):
    """Assign a new subscription plan, deactivating previous plans."""
    self._deactive_plans()
    user_plan = UserPlan(plan=plan, active=True, credit_card=credit_card)
    self.user_plans.append(user_plan)
```

### Repositories

Padrão Repository implementado para abstrair o acesso a dados:

```python
class UserRepository:
    """Repository for creating and querying authentication users."""
    
    async def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email address."""
        result = await self.db.execute(select(User).filter_by(email=email))
        return result.scalar_one_or_none()
```

### Domain Exceptions

Exceções de domínio centralizadas para validação de regras de negócio:

```python
class DomainException(Exception):
    """Base class for all domain-level business rule violations."""
    
    @staticmethod
    def validate(condition: bool, message: str):
        """Raise a DomainException if the condition is not met."""
        if not condition:
            raise DomainException(message)
```

## Arquitetura

### Monolito Modular

O projeto segue a arquitetura de monolito modular, onde cada bounded context é um módulo Python independente:

```
app/
├── authentication/     # Contexto de autenticação
├── subscription/       # Contexto de assinaturas
├── movement/          # Contexto de movimentações
├── infra/             # Infraestrutura compartilhada
└── main.py            # Entry point da aplicação
```

### Comunicação entre Módulos

Os módulos se comunicam através de queries e services, mantendo baixo acoplamento:

```python
# Movement consulta Subscription para validar limites
query_user_plan: QueryUserPlan = Depends(get_query_user_plan)
user_plan = await query_user_plan.execute(email)
```

## Stack Tecnológica

- **Python 3.11+**
- **FastAPI**: Framework web assíncrono
- **SQLAlchemy**: ORM com suporte a async
- **PostgreSQL**: Banco de dados relacional
- **Pydantic**: Validação de dados
- **python-jose**: JWT para autenticação
- **passlib**: Hash de senhas com bcrypt
- **uv**: Gerenciador de pacotes moderno
- **Docker**: Containerização do banco de dados

## Instalação e Execução

### Pré-requisitos

- Python 3.11+
- Docker e Docker Compose
- uv (gerenciador de pacotes)

### Passos

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd track-money
```

2. Crie o arquivo de variáveis de ambiente:
```bash
cp .env.example .env
```

3. Inicie o banco de dados:
```bash
docker compose up -d
```

4. Instale as dependências:
```bash
uv sync
```

5. Execute a aplicação:
```bash
uv run uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

### Seed de Dados Iniciais

Para popular o banco com planos padrão:
```bash
uv run python -m app.infra.seed_plans
```

## Endpoints Principais

### Authentication
- `POST /users` - Registrar novo usuário
- `POST /users/token` - Autenticar e obter JWT
- `GET /users/profile` - Obter perfil do usuário autenticado

### Subscription
- `POST /subscriptions/select-plan` - Selecionar plano de assinatura
- `GET /subscriptions/user` - Consultar usuário e seus planos

### Movement
- `POST /movements/bank-accounts` - Registrar conta bancária

## Decisões de Design

### Por que Monolito Modular?

- **Simplicidade operacional**: Deploy único, sem overhead de microsserviços
- **Coesão alta**: Módulos coesos dentro do mesmo processo
- **Evolução segura**: Fácil extrair módulos para microsserviços no futuro
- **Adequado ao escopo**: Complexidade do domínio não justifica microsserviços

### Por que Async/Await?

- **Performance**: Operações de I/O não bloqueiam a event loop
- **Escalabilidade**: Melhor utilização de recursos em cenários de alta concorrência
- **Modernidade**: Alinhado com as melhores práticas do FastAPI

### Por que Entidades Ricas?

- **Encapsulamento**: Regras de negócio próximas aos dados
- **Validação**: Objetos sempre válidos por construção
- **Manutenibilidade**: Comportamento centralizado na entidade

## Aprendizados

Este projeto demonstra na prática:

- Como identificar e definir Bounded Contexts
- A importância do isolamento de entidades entre contextos
- Como modelar entidades ricas com comportamento
- O uso de Value Objects para conceitos sem identidade
- Implementação do padrão Repository
- Comunicação entre módulos mantendo baixo acoplamento
- Validação de regras de negócio no domínio
- Arquitetura de monolito modular como alternativa a microsserviços

## Licença

Este projeto foi desenvolvido para fins educacionais como parte do curso de DDD da Alura.
