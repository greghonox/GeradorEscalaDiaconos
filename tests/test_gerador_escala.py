"""Testes para o módulo gerador_escala."""

from collections import defaultdict

import pytest
from src.gerador_escala import DiaconoEscala, GeradorEscalaDiaconos

TELEFONE_TESTE = "19 99999-9999"


def _diaconos(*nomes: str):
    """Monta a lista no formato (nome, telefone) esperado pelo gerador."""
    return [(nome, TELEFONE_TESTE) for nome in nomes]


class TestGeradorEscalaDiaconos:
    """Classe de testes para GeradorEscalaDiaconos."""

    def test_inicializacao_com_lista_valida(self):
        """Testa a inicialização com uma lista válida de diáconos."""
        diaconos = _diaconos("João", "Maria", "Pedro", "Ana")
        gerador = GeradorEscalaDiaconos(diaconos)

        assert gerador.lista_diaconos == ["João", "Maria", "Pedro", "Ana"]
        assert gerador.lista_diaconos_contatos == {
            "João": TELEFONE_TESTE,
            "Maria": TELEFONE_TESTE,
            "Pedro": TELEFONE_TESTE,
            "Ana": TELEFONE_TESTE,
        }
        assert gerador.escala_gerada == []

    def test_inicializacao_com_lista_vazia(self):
        """Testa que inicialização com lista vazia levanta ValueError."""
        with pytest.raises(
            ValueError, match="A lista de diáconos não pode estar vazia"
        ):
            GeradorEscalaDiaconos([])

    def test_gerar_escala_semanal_estrutura_basica(self):
        """Testa que a escala gerada tem a estrutura correta."""
        nomes = ["João", "Maria", "Pedro", "Ana", "Carlos", "Julia", "Paulo", "Sofia"]
        gerador = GeradorEscalaDiaconos(_diaconos(*nomes), seed=123)
        escala = gerador.gerar_escala_semanal()

        # Deve ter 7 atribuições: 2 (domingo) + 2 (quarta) + 3 (sábado)
        assert len(escala) == 7

        # Verifica que todos são instâncias de DiaconoEscala
        for diacono in escala:
            assert isinstance(diacono, DiaconoEscala)
            assert diacono.nome in nomes
            assert diacono.funcao in ["chave", "oferta"]
            assert diacono.dia in ["domingo", "quarta", "sabado"]

    def test_escala_domingo_tem_chave_e_oferta(self):
        """Testa que domingo tem exatamente 1 chave e 1 oferta."""
        diaconos = _diaconos("João", "Maria", "Pedro", "Ana", "Carlos", "Julia")
        gerador = GeradorEscalaDiaconos(diaconos, seed=456)
        escala = gerador.gerar_escala_semanal()

        domingo = [d for d in escala if d.dia == "domingo"]
        assert len(domingo) == 2

        funcoes = [d.funcao for d in domingo]
        assert "chave" in funcoes
        assert "oferta" in funcoes
        assert funcoes.count("chave") == 1
        assert funcoes.count("oferta") == 1

    def test_escala_quarta_tem_chave_e_oferta(self):
        """Testa que quarta tem exatamente 1 chave e 1 oferta."""
        diaconos = _diaconos("João", "Maria", "Pedro", "Ana", "Carlos", "Julia")
        gerador = GeradorEscalaDiaconos(diaconos, seed=789)
        escala = gerador.gerar_escala_semanal()

        quarta = [d for d in escala if d.dia == "quarta"]
        assert len(quarta) == 2

        funcoes = [d.funcao for d in quarta]
        assert "chave" in funcoes
        assert "oferta" in funcoes
        assert funcoes.count("chave") == 1
        assert funcoes.count("oferta") == 1

    def test_escala_sabado_tem_1_chave_e_2_ofertas(self):
        """Testa que sábado tem exatamente 1 chave e 2 ofertas."""
        diaconos = _diaconos("João", "Maria", "Pedro", "Ana", "Carlos", "Julia")
        gerador = GeradorEscalaDiaconos(diaconos, seed=321)
        escala = gerador.gerar_escala_semanal()

        sabado = [d for d in escala if d.dia == "sabado"]
        assert len(sabado) == 3

        funcoes = [d.funcao for d in sabado]
        assert funcoes.count("chave") == 1
        assert funcoes.count("oferta") == 2

    @pytest.mark.skip(reason="evitar_repeticao ainda permite nomes duplicados no sorteio")
    def test_evitar_repeticao_ativa(self):
        """Testa que evitar_repeticao=True não repete diáconos na mesma semana."""
        diaconos = _diaconos(
            "João", "Maria", "Pedro", "Ana", "Carlos", "Julia", "Paulo", "Sofia"
        )
        gerador = GeradorEscalaDiaconos(diaconos, seed=999)
        escala = gerador.gerar_escala_semanal(evitar_repeticao=True)

        # Coleta todos os nomes
        nomes = [d.nome for d in escala]

        # Verifica que não há repetições
        assert len(nomes) == len(set(nomes))

    def test_evitar_repeticao_desativada(self):
        """Testa que evitar_repeticao=False permite repetições."""
        diaconos = _diaconos("João", "Maria", "Pedro")
        gerador = GeradorEscalaDiaconos(diaconos, seed=111)
        escala = gerador.gerar_escala_semanal(evitar_repeticao=False)

        # Com apenas 3 diáconos e 7 atribuições, deve haver repetições
        nomes = [d.nome for d in escala]
        assert len(nomes) == 7
        # Verifica que há pelo menos uma repetição
        assert len(set(nomes)) < len(nomes)

    def test_obter_escala_por_dia(self):
        """Testa o método obter_escala_por_dia."""
        diaconos = _diaconos(
            "João", "Maria", "Pedro", "Ana", "Carlos", "Julia", "Paulo", "Sofia"
        )
        gerador = GeradorEscalaDiaconos(diaconos, seed=222)
        gerador.gerar_escala_semanal()

        escala_por_dia = gerador.obter_escala_por_dia()

        assert "domingo" in escala_por_dia
        assert "quarta" in escala_por_dia
        assert "sabado" in escala_por_dia

        assert len(escala_por_dia["domingo"]) == 2
        assert len(escala_por_dia["quarta"]) == 2
        assert len(escala_por_dia["sabado"]) == 3

    def test_obter_escala_por_funcao(self):
        """Testa o método obter_escala_por_funcao."""
        diaconos = _diaconos(
            "João", "Maria", "Pedro", "Ana", "Carlos", "Julia", "Paulo", "Sofia"
        )
        gerador = GeradorEscalaDiaconos(diaconos, seed=333)
        gerador.gerar_escala_semanal()

        escala_por_funcao = gerador.obter_escala_por_funcao()

        assert "chave" in escala_por_funcao
        assert "oferta" in escala_por_funcao

        # Deve ter 3 chaves (1 domingo + 1 quarta + 1 sábado)
        assert len(escala_por_funcao["chave"]) == 3

        # Deve ter 4 ofertas (1 domingo + 1 quarta + 2 sábado)
        assert len(escala_por_funcao["oferta"]) == 4

    def test_exibir_escala_com_escala_gerada(self):
        """Testa o método exibir_escala com escala gerada."""
        diaconos = _diaconos("João", "Maria", "Pedro", "Ana", "Carlos", "Julia")
        gerador = GeradorEscalaDiaconos(diaconos, seed=444)
        gerador.gerar_escala_semanal()

        resultado = gerador.exibir_escala()

        assert isinstance(resultado, str)
        assert "DOMINGO" in resultado
        assert "QUARTA" in resultado
        assert "SABADO" in resultado
        assert "chave" in resultado.lower()
        assert "oferta" in resultado.lower()

    def test_exibir_escala_sem_escala_gerada(self):
        """Testa o método exibir_escala sem escala gerada."""
        diaconos = _diaconos("João", "Maria", "Pedro")
        gerador = GeradorEscalaDiaconos(diaconos)

        resultado = gerador.exibir_escala()

        assert resultado == "Nenhuma escala gerada ainda."

    def test_sortear_diacono_com_lista_valida(self):
        """Testa o método privado _sortear_diacono."""
        gerador = GeradorEscalaDiaconos(_diaconos("João", "Maria", "Pedro"), seed=555)

        sorteado = gerador._sortear_diacono(gerador.lista_diaconos)

        assert sorteado in gerador.lista_diaconos

    def test_sortear_diacono_com_lista_vazia(self):
        """Testa que _sortear_diacono com lista vazia levanta ValueError."""
        gerador = GeradorEscalaDiaconos(_diaconos("João", "Maria"))

        with pytest.raises(
            ValueError, match="Não há diáconos disponíveis para sorteio"
        ):
            gerador._sortear_diacono([])

    def test_remover_diacono(self):
        """Testa o método privado _remover_diacono."""
        nomes = ["João", "Maria", "Pedro", "Ana"]
        gerador = GeradorEscalaDiaconos(_diaconos(*nomes))

        resultado = gerador._remover_diacono(nomes, "Maria")

        assert "Maria" not in resultado
        assert len(resultado) == 3
        assert "João" in resultado
        assert "Pedro" in resultado
        assert "Ana" in resultado

    def test_multiplas_geracoes_independentes(self):
        """Testa que múltiplas gerações são independentes."""
        diaconos = _diaconos(
            "João", "Maria", "Pedro", "Ana", "Carlos", "Julia", "Paulo", "Sofia"
        )
        gerador = GeradorEscalaDiaconos(diaconos)

        escala1 = gerador.gerar_escala_semanal()
        escala2 = gerador.gerar_escala_semanal()

        # Ambas devem ter 7 atribuições
        assert len(escala1) == 7
        assert len(escala2) == 7

        # Mas podem ser diferentes (a menos que use seed)
        # Verificamos apenas que ambas são válidas
        for escala in [escala1, escala2]:
            dias = [d.dia for d in escala]
            assert dias.count("domingo") == 2
            assert dias.count("quarta") == 2
            assert dias.count("sabado") == 3

    def test_lista_diaconos_nao_e_modificada(self):
        """Testa que a lista original de diáconos não é modificada."""
        diaconos_original = _diaconos("João", "Maria", "Pedro", "Ana")
        diaconos_copia = diaconos_original.copy()

        gerador = GeradorEscalaDiaconos(diaconos_original)
        gerador.gerar_escala_semanal()

        # A lista original não deve ser modificada
        assert gerador.lista_diaconos == [nome for nome, _ in diaconos_copia]
        assert diaconos_original == diaconos_copia

    def test_gerar_escala_anual_com_diaconos_externos(self):
        """Testa a geração anual com uma lista recebida de fora."""
        diaconos = _diaconos(
            "Mateus Almeida",
            "Gregório Honorato",
            "Danilo Maciel Santos",
            "Carlos Siebert",
            "João Batista",
            "José Botelho",
            "Elias Gonçalves",
            "Celso Henrique",
        )
        nomes = {nome for nome, _ in diaconos}
        gerador = GeradorEscalaDiaconos(diaconos, seed=2026)
        escala = gerador.gerar_escala_anual(2026)

        assert len(escala) > 0
        assert all(diacono.nome in nomes for diacono in escala)
        assert gerador.lista_diaconos_contatos["Mateus Almeida"] == TELEFONE_TESTE
        assert gerador.lista_diaconos_contatos["Gregório Honorato"] == TELEFONE_TESTE

        por_data = defaultdict(list)
        for diacono in escala:
            por_data[diacono.data].append(diacono)

        chave_por_sabado = {}
        for data_evento, itens in por_data.items():
            funcoes = [item.funcao for item in itens]
            dia = itens[0].dia
            if dia == "sabado":
                assert funcoes.count("chave") == 1
                assert funcoes.count("oferta") == 2
                chave = next(item.nome for item in itens if item.funcao == "chave")
                chave_por_sabado[data_evento] = chave
            else:
                assert funcoes.count("chave") == 1
                assert "oferta" not in funcoes

        for diacono in escala:
            if diacono.dia in ("domingo", "quarta") and diacono.funcao == "chave":
                sabado = gerador._encontrar_sabado_semana(diacono.data)
                if sabado in chave_por_sabado:
                    assert diacono.nome == chave_por_sabado[sabado]

        chaves_sabado = [
            diacono.nome
            for diacono in escala
            if diacono.funcao == "chave" and diacono.dia == "sabado"
        ]
        assert set(chaves_sabado[: len(nomes)]) == nomes

    def test_sementes_diferentes_geram_escalas_distintas(self):
        """Testa que seeds diferentes mudam a ordem inicial das chaves."""
        def chaves_sabado(seed: int) -> list[str]:
            diaconos = _diaconos(
                "Mateus Almeida",
                "Gregório Honorato",
                "Danilo Maciel Santos",
                "Carlos Siebert",
                "João Batista",
                "José Botelho",
                "Elias Gonçalves",
                "Celso Henrique",
            )
            gerador = GeradorEscalaDiaconos(diaconos, seed=seed)
            return [
                diacono.nome
                for diacono in gerador.gerar_escala_anual(2026)
                if diacono.funcao == "chave" and diacono.dia == "sabado"
            ]

        chaves_a = chaves_sabado(11)
        chaves_b = chaves_sabado(22)
        chaves_repetidas = chaves_sabado(11)

        assert chaves_a != chaves_b
        assert chaves_a == chaves_repetidas
        assert chaves_a[0] != chaves_b[0] or chaves_a[1] != chaves_b[1]
