"""Módulo principal do gerador de escala para diáconos."""

from src.gerador_escala import GeradorEscalaDiaconos


def main() -> None:
    """Função principal do aplicativo."""
    print("Gerador de Escala para Diáconos")
    print("=" * 50)

    # Exemplo de uso: gerar escala para o ano 2026
    diaconos = [
        "João",
        "Maria",
        "Pedro",
        "Ana",
        "Carlos",
        "Julia",
        "Paulo",
        "Sofia",
    ]

    ano = 2026
    print(f"\nGerando escala para o ano {ano}...")
    print(f"Diáconos disponíveis: {', '.join(diaconos)}\n")

    gerador = GeradorEscalaDiaconos(diaconos, seed=42)
    escala = gerador.gerar_escala_anual(ano)

    print(f"Total de eventos gerados: {len(escala)}")
    print("\n" + gerador.exibir_escala())


if __name__ == "__main__":
    main()
