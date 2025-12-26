# Gerador de Escala para Diáconos

Projeto para geração de escalas para diáconos.

## Requisitos

- Python 3.12 ou superior
- Poetry (gerenciador de dependências)

## Instalação

1. Instale as dependências do projeto:
```bash
poetry install
```

2. Ative o ambiente virtual:
```bash
poetry shell
```

## Uso

Execute o módulo principal:
```bash
poetry run python -m src.main
```

## Desenvolvimento

### Adicionar dependências

```bash
poetry add nome-do-pacote
```

### Adicionar dependências de desenvolvimento

```bash
poetry add --group dev nome-do-pacote
```

### Atualizar dependências

```bash
poetry update
```

## Estrutura do Projeto

```
GeradorEscalaDiaconos/
├── src/  # Pacote principal
│   ├── __init__.py
│   └── main.py
├── pyproject.toml            # Configuração do Poetry
├── poetry.lock               # Lock file das dependências
└── README.md
```
