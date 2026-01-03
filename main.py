"""Módulo principal do gerador de escala para diáconos."""

from src.gerador_escala import GeradorEscalaDiaconos
from src.gerador_planilha import GeradorPlanilha


def main() -> None:
    """Função principal do aplicativo."""
    print("Gerador de Escala para Diáconos")
    print("=" * 50)

    # Exemplo de uso: gerar escala para o ano 2026
    diaconos = []

    ano = 2026
    print(f"\nGerando escala para o ano {ano}...")
    print(f"Diáconos disponíveis: {', '.join([nome for nome, _ in diaconos])}\n")

    gerador = GeradorEscalaDiaconos(diaconos)
    escala = gerador.gerar_escala_anual(ano)

    print(f"Total de eventos gerados: {len(escala)}")
    print("\n" + gerador.exibir_escala())

    # Gera a planilha Excel
    print("\n" + "=" * 50)
    print("Gerando planilha Excel...")
    gerador_planilha = GeradorPlanilha(escala, ano, diaconos, seed=gerador.seed)
    caminho_arquivo = f"/tmp/escala_diaconos_{ano}.xlsx"
    gerador_planilha.gerar_planilha(caminho_arquivo)
    print(f"Planilha salva em: {caminho_arquivo}")


def main_many_sheets():
    """Função principal do aplicativo para gerar planilhas para múltiplos anos."""
    print("Gerador de Escala para Diáconos")
    print("=" * 50)

    # Exemplo de uso: gerar escala para o ano 2026
    diaconos = []

    ano = 2026
    for n in range(5):
        gerador = GeradorEscalaDiaconos(diaconos)
        escala = gerador.gerar_escala_anual(ano)
        gerador_planilha = GeradorPlanilha(escala, ano, diaconos, seed=gerador.seed)
        caminho_arquivo = f"/tmp/escala_diaconos_{ano}_{n}.xlsx"
        gerador_planilha.gerar_planilha(caminho_arquivo)


if __name__ == "__main__":
    main_many_sheets()
