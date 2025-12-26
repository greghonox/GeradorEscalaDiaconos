"""Módulo principal do gerador de escala para diáconos."""

from src.gerador_escala import GeradorEscalaDiaconos
from src.gerador_planilha import GeradorPlanilha


def main() -> None:
    """Função principal do aplicativo."""
    print("Gerador de Escala para Diáconos")
    print("=" * 50)

    # Exemplo de uso: gerar escala para o ano 2026
    diaconos = [
        ("Gregório Honorato", "19 99250-9913"),
        ("Danilo Maciel Santos", "19 98838-2727"),
        ("Carlos Siebert", "19 99194-2389"),
        ("João Batista", "19 98930-3939"),
        ("José Botelho", "19 98131-0842"),
        ("Ivaldo Da Silva", "19 99412-2468"),
        ("Elias Gonçalves", "19 98209-2483"),
        ("Celso Henrique", "19 99127-2067"),
    ]

    ano = 2026
    print(f"\nGerando escala para o ano {ano}...")
    print(f"Diáconos disponíveis: {', '.join([nome for nome, _ in diaconos])}\n")

    gerador = GeradorEscalaDiaconos(diaconos, seed=42)
    escala = gerador.gerar_escala_anual(ano)

    print(f"Total de eventos gerados: {len(escala)}")
    print("\n" + gerador.exibir_escala())

    # Gera a planilha Excel
    print("\n" + "=" * 50)
    print("Gerando planilha Excel...")
    gerador_planilha = GeradorPlanilha(escala, ano, diaconos)
    caminho_arquivo = f"/tmp/escala_diaconos_{ano}.xlsx"
    gerador_planilha.gerar_planilha(caminho_arquivo)
    print(f"Planilha salva em: {caminho_arquivo}")


if __name__ == "__main__":
    main()
