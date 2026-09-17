"""Carrega a lista de diáconos de um arquivo JSON externo."""

from pathlib import Path
from typing import List, Tuple

import json

CaminhoDiaconos = str | Path
ListaDiaconos = List[Tuple[str, str]]


def caminho_padrao() -> Path:
    """Retorna o JSON de diáconos na raiz do projeto."""
    return Path(__file__).resolve().parent.parent / "diaconos.json"


def carregar_diaconos(caminho: CaminhoDiaconos | None = None) -> ListaDiaconos:
    """
    Lê a lista de diáconos de um JSON no formato
    [{"nome": "...", "telefone": "..."}, ...].
    """
    arquivo = Path(caminho) if caminho is not None else caminho_padrao()
    if not arquivo.is_file():
        raise FileNotFoundError(f"Arquivo de diáconos não encontrado: {arquivo}")

    with arquivo.open(encoding="utf-8") as handle:
        dados = json.load(handle)

    if not isinstance(dados, list) or not dados:
        raise ValueError("A lista de diáconos não pode estar vazia")

    diaconos: ListaDiaconos = []
    for item in dados:
        nome = str(item.get("nome", "")).strip()
        telefone = str(item.get("telefone", "")).strip()
        if not nome or not telefone:
            raise ValueError(
                "Cada diácono precisa de nome e telefone no arquivo JSON"
            )
        diaconos.append((nome, telefone))

    return diaconos
