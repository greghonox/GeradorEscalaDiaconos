"""Testes para o módulo gerador_escala."""

import pytest
from src.gerador_escala import GeradorEscalaDiaconos, DiaconoEscala


class TestGeradorEscalaDiaconos:
    """Classe de testes para GeradorEscalaDiaconos."""

    def test_inicializacao_com_lista_valida(self):
        """Testa a inicialização com uma lista válida de diáconos."""
        diaconos = ["João", "Maria", "Pedro", "Ana"]
        gerador = GeradorEscalaDiaconos(diaconos)

        assert gerador.lista_diaconos == diaconos
        assert gerador.escala_gerada == []

    def test_inicializacao_com_lista_vazia(self):
        """Testa que inicialização com lista vazia levanta ValueError."""
        with pytest.raises(
            ValueError, match="A lista de diáconos não pode estar vazia"
        ):
            GeradorEscalaDiaconos([])

    def test_gerar_escala_semanal_estrutura_basica(self):
        """Testa que a escala gerada tem a estrutura correta."""
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
        gerador = GeradorEscalaDiaconos(diaconos, seed=123)
        escala = gerador.gerar_escala_semanal()

        # Deve ter 7 atribuições: 2 (domingo) + 2 (quarta) + 3 (sábado)
        assert len(escala) == 7

        # Verifica que todos são instâncias de DiaconoEscala
        for diacono in escala:
            assert isinstance(diacono, DiaconoEscala)
            assert diacono.nome in diaconos
            assert diacono.funcao in ["chave", "oferta"]
            assert diacono.dia in ["domingo", "quarta", "sabado"]

    def test_escala_domingo_tem_chave_e_oferta(self):
        """Testa que domingo tem exatamente 1 chave e 1 oferta."""
        diaconos = ["João", "Maria", "Pedro", "Ana", "Carlos", "Julia"]
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
        diaconos = ["João", "Maria", "Pedro", "Ana", "Carlos", "Julia"]
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
        diaconos = ["João", "Maria", "Pedro", "Ana", "Carlos", "Julia"]
        gerador = GeradorEscalaDiaconos(diaconos, seed=321)
        escala = gerador.gerar_escala_semanal()

        sabado = [d for d in escala if d.dia == "sabado"]
        assert len(sabado) == 3

        funcoes = [d.funcao for d in sabado]
        assert funcoes.count("chave") == 1
        assert funcoes.count("oferta") == 2

    @pytest.mark.disable_test
    def test_evitar_repeticao_ativa(self):
        """Testa que evitar_repeticao=True não repete diáconos na mesma semana."""
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
        gerador = GeradorEscalaDiaconos(diaconos, seed=999)
        escala = gerador.gerar_escala_semanal(evitar_repeticao=True)

        # Coleta todos os nomes
        nomes = [d.nome for d in escala]

        # Verifica que não há repetições
        assert len(nomes) == len(set(nomes))

    def test_evitar_repeticao_desativada(self):
        """Testa que evitar_repeticao=False permite repetições."""
        diaconos = ["João", "Maria", "Pedro"]
        gerador = GeradorEscalaDiaconos(diaconos, seed=111)
        escala = gerador.gerar_escala_semanal(evitar_repeticao=False)

        # Com apenas 3 diáconos e 7 atribuições, deve haver repetições
        nomes = [d.nome for d in escala]
        assert len(nomes) == 7
        # Verifica que há pelo menos uma repetição
        assert len(set(nomes)) < len(nomes)

    def test_obter_escala_por_dia(self):
        """Testa o método obter_escala_por_dia."""
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
        diaconos = ["João", "Maria", "Pedro", "Ana", "Carlos", "Julia"]
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
        diaconos = ["João", "Maria", "Pedro"]
        gerador = GeradorEscalaDiaconos(diaconos)

        resultado = gerador.exibir_escala()

        assert resultado == "Nenhuma escala gerada ainda."

    def test_sortear_diacono_com_lista_valida(self):
        """Testa o método privado _sortear_diacono."""
        diaconos = ["João", "Maria", "Pedro"]
        gerador = GeradorEscalaDiaconos(diaconos, seed=555)

        sorteado = gerador._sortear_diacono(diaconos)

        assert sorteado in diaconos

    def test_sortear_diacono_com_lista_vazia(self):
        """Testa que _sortear_diacono com lista vazia levanta ValueError."""
        diaconos = ["João", "Maria"]
        gerador = GeradorEscalaDiaconos(diaconos)

        with pytest.raises(
            ValueError, match="Não há diáconos disponíveis para sorteio"
        ):
            gerador._sortear_diacono([])

    def test_remover_diacono(self):
        """Testa o método privado _remover_diacono."""
        diaconos = ["João", "Maria", "Pedro", "Ana"]
        gerador = GeradorEscalaDiaconos(diaconos)

        resultado = gerador._remover_diacono(diaconos, "Maria")

        assert "Maria" not in resultado
        assert len(resultado) == 3
        assert "João" in resultado
        assert "Pedro" in resultado
        assert "Ana" in resultado

    def test_multiplas_geracoes_independentes(self):
        """Testa que múltiplas gerações são independentes."""
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
        diaconos_original = ["João", "Maria", "Pedro", "Ana"]
        diaconos_copia = diaconos_original.copy()

        gerador = GeradorEscalaDiaconos(diaconos_original)
        gerador.gerar_escala_semanal()

        # A lista original não deve ser modificada
        assert gerador.lista_diaconos == diaconos_copia
        assert diaconos_original == diaconos_copia
