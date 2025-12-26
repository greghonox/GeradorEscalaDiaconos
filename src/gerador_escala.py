"""Módulo para geração de escala de diáconos."""

import random
from datetime import timedelta, date
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class DiaconoEscala:
    """Representa um diácono na escala."""

    nome: str
    funcao: str  # 'chave' ou 'oferta'
    dia: str
    data: Optional[date] = None  # Data do evento


class GeradorEscalaDiaconos:
    """Classe para gerar escala de diáconos através de sorteio."""

    DIAS_ESCALA = ["domingo", "quarta", "sabado"]
    MAPA_DIAS_SEMANA = {
        "domingo": 6,  # 0=segunda, 6=domingo
        "quarta": 2,  # 2=quarta
        "sabado": 5,  # 5=sábado
    }

    def __init__(self, lista_diaconos: List[str], seed: Optional[int] = None):
        """
        Inicializa o gerador de escala.

        Args:
            lista_diaconos: Lista com os nomes dos diáconos disponíveis
            seed: Semente opcional para reproduzibilidade dos sorteios
        """
        if not lista_diaconos:
            raise ValueError("A lista de diáconos não pode estar vazia")

        self.lista_diaconos = lista_diaconos.copy()
        self.escala_gerada: List[DiaconoEscala] = []
        # Rastreamento de rotação circular para função "chave"
        self._chaves_usadas: List[str] = []
        # Mapeia a data do sábado para o diácono escolhido para chave
        self._chave_semanal: Dict[date, str] = {}

        if seed is not None:
            random.seed(seed)

    def _sortear_diacono(self, diaconos_disponiveis: List[str]) -> str:
        """
        Sorteia um diácono da lista disponível.

        Args:
            diaconos_disponiveis: Lista de diáconos disponíveis para sorteio

        Returns:
            Nome do diácono sorteado
        """
        if not diaconos_disponiveis:
            raise ValueError("Não há diáconos disponíveis para sorteio")

        return random.choice(diaconos_disponiveis)

    def _remover_diacono(self, lista: List[str], nome: str) -> List[str]:
        """
        Remove um diácono da lista.

        Args:
            lista: Lista de diáconos
            nome: Nome do diácono a ser removido

        Returns:
            Nova lista sem o diácono removido
        """
        return [d for d in lista if d != nome]

    def _calcular_datas_ano(self, ano: int) -> Dict[str, List[date]]:
        """
        Calcula todas as datas de domingo, quarta e sábado para um ano.

        Args:
            ano: Ano para calcular as datas

        Returns:
            Dicionário com listas de datas por dia da semana
        """
        datas_por_dia: Dict[str, List[date]] = {
            "domingo": [],
            "quarta": [],
            "sabado": [],
        }

        # Começa no primeiro dia do ano
        data_atual = date(ano, 1, 1)
        # Vai até o último dia do ano
        data_fim = date(ano, 12, 31)

        while data_atual <= data_fim:
            dia_semana = data_atual.weekday()  # 0=segunda, 6=domingo

            if dia_semana == self.MAPA_DIAS_SEMANA["domingo"]:
                datas_por_dia["domingo"].append(data_atual)
            elif dia_semana == self.MAPA_DIAS_SEMANA["quarta"]:
                datas_por_dia["quarta"].append(data_atual)
            elif dia_semana == self.MAPA_DIAS_SEMANA["sabado"]:
                datas_por_dia["sabado"].append(data_atual)

            data_atual += timedelta(days=1)

        return datas_por_dia

    def _obter_proximo_chave_circular(self) -> str:
        """
        Obtém o próximo diácono para função chave usando rotação circular.
        Só repete um diácono após todos terem sido escolhidos.

        Returns:
            Nome do próximo diácono para chave
        """
        # Se todos já foram usados, reinicia a lista
        if len(self._chaves_usadas) >= len(self.lista_diaconos):
            self._chaves_usadas = []

        # Encontra diáconos ainda não usados nesta rodada
        diaconos_disponiveis = [
            d for d in self.lista_diaconos if d not in self._chaves_usadas
        ]

        # Se não há disponíveis (não deveria acontecer), reinicia
        if not diaconos_disponiveis:
            self._chaves_usadas = []
            diaconos_disponiveis = self.lista_diaconos.copy()

        # Sorteia um dos disponíveis
        escolhido = random.choice(diaconos_disponiveis)
        self._chaves_usadas.append(escolhido)

        return escolhido

    def _encontrar_sabado_semana(self, data_evento: date) -> Optional[date]:
        """
        Encontra o sábado anterior da mesma semana de uma data.
        O sábado escolhido é usado no domingo e quarta da mesma semana.

        Args:
            data_evento: Data do evento (domingo ou quarta)

        Returns:
            Data do sábado anterior da mesma semana, ou None se não encontrado
        """
        # weekday: 0=segunda, 1=terça, 2=quarta, 3=quinta,
        # 4=sexta, 5=sábado, 6=domingo
        dia_semana = data_evento.weekday()

        if dia_semana == 6:  # Domingo
            # Domingo: o sábado anterior é 1 dia antes
            dias_ate_sabado = -1
        elif dia_semana == 2:  # Quarta
            # Quarta: o sábado anterior é 4 dias antes
            dias_ate_sabado = -4
        else:
            return None

        sabado = data_evento + timedelta(days=dias_ate_sabado)
        return sabado

    def gerar_escala_anual(self, ano: int) -> List[DiaconoEscala]:
        """
        Gera a escala anual completa para um ano específico.

        Args:
            ano: Ano para gerar a escala (ex: 2026)

        Returns:
            Lista com a escala gerada para todo o ano
        """
        self.escala_gerada = []
        self._chaves_usadas = []  # Reinicia o rastreamento de chaves
        self._chave_semanal = {}  # Reinicia o mapeamento semanal

        # Calcula todas as datas do ano
        datas_por_dia = self._calcular_datas_ano(ano)

        # Ordena todas as datas para processar em ordem cronológica
        todas_datas: List[Tuple[date, str]] = []
        for dia, datas in datas_por_dia.items():
            for data in datas:
                todas_datas.append((data, dia))

        todas_datas.sort(key=lambda x: x[0])

        # Processa cada data em ordem cronológica
        for data_evento, dia_semana in todas_datas:
            if dia_semana == "sabado":
                self._adicionar_escala_sabado_anual(data_evento)
            else:
                self._adicionar_escala_dia_anual(dia_semana, data_evento)

        return self.escala_gerada

    def gerar_escala_semanal(
        self, evitar_repeticao: bool = True
    ) -> List[DiaconoEscala]:
        """
        Gera a escala semanal completa (método legado).

        Args:
            evitar_repeticao: Se True, evita que o mesmo diácono seja sorteado
                             mais de uma vez na mesma semana

        Returns:
            Lista com a escala gerada
        """
        self.escala_gerada = []
        self._chaves_usadas = []
        diaconos_disponiveis = self.lista_diaconos.copy()

        # Domingo: 1 para chave, 1 para oferta
        self._adicionar_escala_dia("domingo", diaconos_disponiveis, evitar_repeticao)

        # Quarta: 1 para chave, 1 para oferta
        self._adicionar_escala_dia("quarta", diaconos_disponiveis, evitar_repeticao)

        # Sábado: 1 para chave (seguir na semana), 2 para oferta
        self._adicionar_escala_sabado(diaconos_disponiveis, evitar_repeticao)

        return self.escala_gerada

    def _adicionar_escala_dia_anual(self, dia: str, data_evento: date):
        """
        Adiciona escala para domingo ou quarta no formato anual.
        Apenas chave, sem oferta.
        Usa a mesma pessoa escolhida no sábado da mesma semana.

        Args:
            dia: Nome do dia ('domingo' ou 'quarta')
            data_evento: Data do evento
        """
        # Encontra o sábado da mesma semana
        sabado_semana = self._encontrar_sabado_semana(data_evento)

        if sabado_semana and sabado_semana in self._chave_semanal:
            # Usa a mesma pessoa do sábado da semana
            diacono_chave = self._chave_semanal[sabado_semana]
        else:
            # Se não encontrou o sábado (não deveria acontecer),
            # usa rotação circular
            diacono_chave = self._obter_proximo_chave_circular()

        self.escala_gerada.append(
            DiaconoEscala(nome=diacono_chave, funcao="chave", dia=dia, data=data_evento)
        )

    def _adicionar_escala_dia(
        self, dia: str, diaconos_disponiveis: List[str], evitar_repeticao: bool
    ):
        """
        Adiciona escala para domingo ou quarta (método legado).

        Args:
            dia: Nome do dia ('domingo' ou 'quarta')
            diaconos_disponiveis: Lista de diáconos disponíveis
            evitar_repeticao: Se True, remove diáconos sorteados da lista
        """
        # Sorteia diácono para chave
        diacono_chave = self._sortear_diacono(diaconos_disponiveis)
        self.escala_gerada.append(
            DiaconoEscala(nome=diacono_chave, funcao="chave", dia=dia)
        )

        if evitar_repeticao:
            diaconos_disponiveis = self._remover_diacono(
                diaconos_disponiveis, diacono_chave
            )

        # Sorteia diácono para oferta
        diacono_oferta = self._sortear_diacono(diaconos_disponiveis)
        self.escala_gerada.append(
            DiaconoEscala(nome=diacono_oferta, funcao="oferta", dia=dia)
        )

        if evitar_repeticao:
            diaconos_disponiveis.remove(diacono_oferta)

    def _adicionar_escala_sabado_anual(self, data_evento: date):
        """
        Adiciona escala para sábado no formato anual (1 chave + 2 ofertas).
        Guarda a pessoa escolhida para usar no domingo e quarta da mesma
        semana.

        Args:
            data_evento: Data do evento
        """
        # Usa rotação circular para chave
        diacono_chave = self._obter_proximo_chave_circular()

        # Guarda para usar no domingo e quarta da mesma semana
        self._chave_semanal[data_evento] = diacono_chave

        self.escala_gerada.append(
            DiaconoEscala(
                nome=diacono_chave, funcao="chave", dia="sabado", data=data_evento
            )
        )

        # Sorteia 2 diáconos para oferta (podem ser qualquer um)
        for _ in range(2):
            diacono_oferta = self._sortear_diacono(self.lista_diaconos)
            self.escala_gerada.append(
                DiaconoEscala(
                    nome=diacono_oferta, funcao="oferta", dia="sabado", data=data_evento
                )
            )

    def _adicionar_escala_sabado(
        self, diaconos_disponiveis: List[str], evitar_repeticao: bool
    ):
        """
        Adiciona escala para sábado (1 chave + 2 ofertas) (método legado).

        Args:
            diaconos_disponiveis: Lista de diáconos disponíveis
            evitar_repeticao: Se True, remove diáconos sorteados da lista
        """
        # Sorteia diácono para chave (seguir na semana)
        diacono_chave = self._sortear_diacono(diaconos_disponiveis)
        self.escala_gerada.append(
            DiaconoEscala(nome=diacono_chave, funcao="chave", dia="sabado")
        )

        if evitar_repeticao:
            diaconos_disponiveis = self._remover_diacono(
                diaconos_disponiveis, diacono_chave
            )

        # Sorteia 2 diáconos para oferta
        for _ in range(2):
            diacono_oferta = self._sortear_diacono(diaconos_disponiveis)
            self.escala_gerada.append(
                DiaconoEscala(nome=diacono_oferta, funcao="oferta", dia="sabado")
            )

            if evitar_repeticao:
                diaconos_disponiveis = self._remover_diacono(
                    diaconos_disponiveis, diacono_oferta
                )

    def obter_escala_por_dia(self) -> Dict[str, List[DiaconoEscala]]:
        """
        Retorna a escala organizada por dia.

        Returns:
            Dicionário com a escala agrupada por dia
        """
        escala_por_dia: Dict[str, List[DiaconoEscala]] = {
            dia: [] for dia in self.DIAS_ESCALA
        }

        for diacono in self.escala_gerada:
            escala_por_dia[diacono.dia].append(diacono)

        return escala_por_dia

    def obter_escala_por_funcao(self) -> Dict[str, List[DiaconoEscala]]:
        """
        Retorna a escala organizada por função.

        Returns:
            Dicionário com a escala agrupada por função
        """
        escala_por_funcao: Dict[str, List[DiaconoEscala]] = {"chave": [], "oferta": []}

        for diacono in self.escala_gerada:
            escala_por_funcao[diacono.funcao].append(diacono)

        return escala_por_funcao

    def exibir_escala(self) -> str:
        """
        Retorna uma representação textual da escala.

        Returns:
            String formatada com a escala
        """
        if not self.escala_gerada:
            return "Nenhuma escala gerada ainda."

        # Se tem datas, organiza por data, senão organiza por dia
        if self.escala_gerada[0].data is not None:
            # Organiza por data
            escala_por_data: Dict[date, List[DiaconoEscala]] = {}
            for diacono in self.escala_gerada:
                if diacono.data is not None:
                    if diacono.data not in escala_por_data:
                        escala_por_data[diacono.data] = []
                    escala_por_data[diacono.data].append(diacono)

            resultado = []
            for data in sorted(escala_por_data.keys()):
                dia_semana = self._obter_nome_dia_semana(data.weekday())
                resultado.append(
                    f"\n{data.strftime('%d/%m/%Y')} ({dia_semana.upper()}):"
                )
                for diacono in escala_por_data[data]:
                    resultado.append(f"  - {diacono.nome} ({diacono.funcao})")
        else:
            # Formato legado (sem datas)
            escala_por_dia = self.obter_escala_por_dia()
            resultado = []

            for dia in self.DIAS_ESCALA:
                if dia in escala_por_dia and escala_por_dia[dia]:
                    resultado.append(f"\n{dia.upper()}:")
                    for diacono in escala_por_dia[dia]:
                        resultado.append(f"  - {diacono.nome} ({diacono.funcao})")

        return "\n".join(resultado)

    def _obter_nome_dia_semana(self, weekday: int) -> str:
        """
        Converte weekday (0=segunda, 6=domingo) para nome do dia.

        Args:
            weekday: Número do dia da semana

        Returns:
            Nome do dia da semana
        """
        nomes = {
            0: "segunda",
            1: "terca",
            2: "quarta",
            3: "quinta",
            4: "sexta",
            5: "sabado",
            6: "domingo",
        }
        return nomes.get(weekday, "")
