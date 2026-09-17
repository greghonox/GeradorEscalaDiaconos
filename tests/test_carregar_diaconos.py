"""Testes para o carregamento da lista externa de diáconos."""

import json

import pytest
from src.carregar_diaconos import carregar_diaconos


def test_carregar_diaconos_de_arquivo(tmp_path):
    arquivo = tmp_path / "diaconos.json"
    arquivo.write_text(
        json.dumps(
            [
                {"nome": "João", "telefone": "19 99999-0001"},
                {"nome": "Maria", "telefone": "19 99999-0002"},
            ]
        ),
        encoding="utf-8",
    )

    diaconos = carregar_diaconos(arquivo)

    assert diaconos == [("João", "19 99999-0001"), ("Maria", "19 99999-0002")]


def test_carregar_diaconos_arquivo_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError):
        carregar_diaconos(tmp_path / "nao_existe.json")


def test_carregar_diaconos_lista_vazia(tmp_path):
    arquivo = tmp_path / "diaconos.json"
    arquivo.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="não pode estar vazia"):
        carregar_diaconos(arquivo)
