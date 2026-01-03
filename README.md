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

### Interface Web (Streamlit) - Recomendado

Execute a aplicação Streamlit:
```bash
poetry run streamlit run app.py
```

A aplicação abrirá automaticamente no navegador. Você poderá:
- Gerenciar a lista de diáconos (adicionar/remover)
- Configurar o ano da escala
- Gerar a escala anual
- Visualizar a escala em diferentes formatos
- Baixar a planilha Excel gerada

### Linha de Comando

Execute o módulo principal:
```bash
poetry run python main.py
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
├── src/                      # Pacote principal
│   ├── __init__.py
│   ├── gerador_escala.py     # Lógica de geração de escala
│   └── gerador_planilha.py   # Geração de planilhas Excel
├── app.py                    # Interface web Streamlit
├── main.py                   # Script de linha de comando
├── pyproject.toml            # Configuração do Poetry
├── poetry.lock               # Lock file das dependências
└── README.md
```
