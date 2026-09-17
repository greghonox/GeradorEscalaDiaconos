"""Módulo principal do gerador de escala para diáconos."""

import random
import sys
from pathlib import Path

from src.carregar_diaconos import carregar_diaconos, caminho_padrao
from src.gerador_escala import GeradorEscalaDiaconos
from src.gerador_planilha import GeradorPlanilha


def _caminho_lista() -> Path:
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    return caminho_padrao()


def main() -> None:
    """Função principal do aplicativo."""
    print("Gerador de Escala para Diáconos")
    print("=" * 50)

    caminho = _caminho_lista()
    diaconos = carregar_diaconos(caminho)

    ano = 2026
    print(f"\nLista carregada de: {caminho}")
    print(f"Gerando escala para o ano {ano}...")
    print(f"Diáconos disponíveis: {', '.join([nome for nome, _ in diaconos])}\n")

    gerador = GeradorEscalaDiaconos(diaconos)
    escala = gerador.gerar_escala_anual(ano)

    print(f"Total de eventos gerados: {len(escala)}")
    print("\n" + gerador.exibir_escala())

    print("\n" + "=" * 50)
    print("Gerando planilha Excel...")
    gerador_planilha = GeradorPlanilha(escala, ano, diaconos, seed=gerador.seed)
    caminho_arquivo = f"/tmp/escala_diaconos_{ano}.xlsx"
    gerador_planilha.gerar_planilha(caminho_arquivo)
    print(f"Planilha salva em: {caminho_arquivo}")


def main_many_sheets():
    """Gera várias planilhas com seeds diferentes para o mesmo ano."""
    print("Gerador de Escala para Diáconos")
    print("=" * 50)

    caminho = _caminho_lista()
    diaconos = carregar_diaconos(caminho)
    print(f"Lista carregada de: {caminho}")

    ano = 2026
    seeds = random.sample(range(1, 1_000_000), 10)
    for n, seed in enumerate(seeds):
        gerador = GeradorEscalaDiaconos(diaconos, seed=seed)
        escala = gerador.gerar_escala_anual(ano)
        gerador_planilha = GeradorPlanilha(escala, ano, diaconos, seed=gerador.seed)
        caminho_arquivo = f"/tmp/escala_diaconos_{ano}_{n}.xlsx"
        gerador_planilha.gerar_planilha(caminho_arquivo)
        print(f"Planilha {n}: {caminho_arquivo} (seed {gerador.seed})")


if __name__ == "__main__":
    main_many_sheets()
