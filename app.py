"""Aplicação Streamlit para geração de escala de diáconos."""

import streamlit as st
import io
from datetime import date

from src.gerador_escala import GeradorEscalaDiaconos
from src.gerador_planilha import GeradorPlanilha


def inicializar_sessao():
    """Inicializa variáveis de sessão se não existirem."""
    if "diaconos" not in st.session_state:
        st.session_state.diaconos = [
            ("Gregório Honorato", "19 99250-9913"),
            ("Diacono Teste", "19 99999-9999"),
            ("Diacono Teste 2", "19 99999-9999"),
        ]
    if "escala_gerada" not in st.session_state:
        st.session_state.escala_gerada = None
    if "ano" not in st.session_state:
        st.session_state.ano = date.today().year + 1
    if "seed" not in st.session_state:
        st.session_state.seed = None


def adicionar_diacono(nome: str, telefone: str):
    """Adiciona um diácono à lista."""
    if nome and telefone:
        novo_diacono = (nome.strip(), telefone.strip())
        if novo_diacono not in st.session_state.diaconos:
            st.session_state.diaconos.append(novo_diacono)
            return True
    return False


def remover_diacono(indice: int):
    """Remove um diácono da lista."""
    if 0 <= indice < len(st.session_state.diaconos):
        st.session_state.diaconos.pop(indice)
        return True
    return False


def gerar_escala(ano: int, seed: int = None):
    """Gera a escala anual."""
    if not st.session_state.diaconos:
        st.error("Adicione pelo menos um diácono antes de gerar a escala.")
        return None

    try:
        gerador = GeradorEscalaDiaconos(st.session_state.diaconos, seed=seed)
        escala = gerador.gerar_escala_anual(ano)
        st.session_state.seed = gerador.seed
        return escala, gerador
    except Exception as e:
        st.error(f"Erro ao gerar escala: {str(e)}")
        return None


def main():
    """Função principal da aplicação Streamlit."""
    st.set_page_config(
        page_title="Gerador de Escala para Diáconos",
        page_icon="⛪",
        layout="wide",
    )

    inicializar_sessao()

    # Título principal
    st.title("⛪ Gerador de Escala para Diáconos")
    st.markdown("---")

    # Sidebar para configurações
    with st.sidebar:
        st.header("⚙️ Configurações")

        # Ano
        ano_selecionado = st.number_input(
            "Ano da Escala",
            min_value=2020,
            max_value=2100,
            value=st.session_state.ano,
            step=1,
        )
        st.session_state.ano = ano_selecionado

        # Seed (opcional)
        usar_seed = st.checkbox("Usar seed personalizado", value=False)
        seed_input = None
        if usar_seed:
            seed_input = st.number_input(
                "Seed (para reproduzibilidade)",
                min_value=1,
                max_value=1000000,
                value=st.session_state.seed or 12345,
                step=1,
            )

        st.markdown("---")

        # Botão para gerar escala
        if st.button("🔄 Gerar Escala", type="primary", use_container_width=True):
            resultado = gerar_escala(ano_selecionado, seed_input)
            if resultado:
                escala, gerador = resultado
                st.session_state.escala_gerada = (escala, gerador)
                st.success("Escala gerada com sucesso!")
                st.rerun()

        if st.session_state.seed:
            st.info(f"Seed usado: {st.session_state.seed}")

    # Abas principais
    tab1, tab2, tab3, tab4 = st.tabs(
        ["👥 Diáconos", "📅 Escala", "📊 Visualização", "📞 Contatos"]
    )

    # Aba 1: Gerenciamento de Diáconos
    with tab1:
        st.header("Gerenciar Diáconos")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Adicionar Novo Diácono")
            nome_novo = st.text_input("Nome do Diácono", key="nome_input")
            telefone_novo = st.text_input("Telefone", key="telefone_input")

            col_add1, _ = st.columns([1, 3])
            with col_add1:
                if st.button("➕ Adicionar", use_container_width=True):
                    if adicionar_diacono(nome_novo, telefone_novo):
                        st.success(f"Diácono {nome_novo} adicionado!")
                        st.rerun()
                    else:
                        st.warning(
                            "Preencha nome e telefone, ou o diácono já existe na lista."
                        )

        with col2:
            st.subheader("Estatísticas")
            st.metric("Total de Diáconos", len(st.session_state.diaconos))

        st.markdown("---")
        st.subheader("Lista de Diáconos")

        if st.session_state.diaconos:
            # Tabela de diáconos
            for idx, (nome, telefone) in enumerate(st.session_state.diaconos):
                col_nome, col_tel, col_btn = st.columns([3, 2, 1])
                with col_nome:
                    st.write(f"**{nome}**")
                with col_tel:
                    st.write(telefone)
                with col_btn:
                    if st.button("🗑️", key=f"remover_{idx}", help="Remover"):
                        remover_diacono(idx)
                        st.rerun()
        else:
            st.info("Nenhum diácono adicionado ainda. Adicione diáconos acima.")

    # Aba 2: Escala Gerada
    with tab2:
        st.header(f"Escala para o Ano {st.session_state.ano}")

        if st.session_state.escala_gerada is None:
            st.info(
                "👈 Use o botão 'Gerar Escala' na barra lateral para gerar a escala."
            )
        else:
            escala, gerador = st.session_state.escala_gerada

            st.success(f"✅ Escala gerada com {len(escala)} eventos")

            # Exibir escala formatada
            st.subheader("Escala Completa")
            escala_texto = gerador.exibir_escala()
            st.text(escala_texto)

            # Botão para download da planilha
            st.markdown("---")
            st.subheader("Download da Planilha Excel")

            if st.button("📥 Gerar e Baixar Planilha Excel", type="primary"):
                try:
                    # Cria a planilha em memória
                    gerador_planilha = GeradorPlanilha(
                        escala,
                        st.session_state.ano,
                        st.session_state.diaconos,
                        seed=st.session_state.seed,
                    )

                    # Salva em buffer
                    buffer = io.BytesIO()
                    gerador_planilha.gerar_planilha(buffer)
                    buffer.seek(0)

                    # Nome do arquivo
                    nome_arquivo = f"escala_diaconos_{st.session_state.ano}.xlsx"

                    # Botão de download
                    st.download_button(
                        label="⬇️ Baixar Planilha",
                        data=buffer,
                        file_name=nome_arquivo,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                except Exception as e:
                    st.error(f"Erro ao gerar planilha: {str(e)}")

    # Aba 3: Visualização Detalhada
    with tab3:
        st.header("Visualização Detalhada da Escala")

        if st.session_state.escala_gerada is None:
            st.info("👈 Gere a escala primeiro usando o botão na barra lateral.")
        else:
            escala, gerador = st.session_state.escala_gerada

            # Filtros
            col_filtro1, col_filtro2 = st.columns(2)

            with col_filtro1:
                dias_filtro = st.multiselect(
                    "Filtrar por dia",
                    options=["domingo", "quarta", "sabado"],
                    default=["domingo", "quarta", "sabado"],
                )

            with col_filtro2:
                funcoes_filtro = st.multiselect(
                    "Filtrar por função",
                    options=["chave", "oferta"],
                    default=["chave", "oferta"],
                )

            # Aplicar filtros
            escala_filtrada = [
                d for d in escala if d.dia in dias_filtro and d.funcao in funcoes_filtro
            ]

            if escala_filtrada:
                # Organizar por data
                escala_por_data = {}
                for diacono in escala_filtrada:
                    if diacono.data:
                        if diacono.data not in escala_por_data:
                            escala_por_data[diacono.data] = {
                                "chave": [],
                                "oferta": [],
                                "dia": diacono.dia,
                            }
                        escala_por_data[diacono.data][diacono.funcao].append(
                            diacono.nome
                        )

                # Exibir em formato de tabela
                st.subheader(f"Eventos Filtrados ({len(escala_filtrada)} eventos)")

                dados_tabela = []
                for data_evento in sorted(escala_por_data.keys()):
                    dados = escala_por_data[data_evento]
                    dados_tabela.append(
                        {
                            "Data": data_evento.strftime("%d/%m/%Y"),
                            "Dia": dados["dia"].upper(),
                            "Chave": (
                                " / ".join(dados["chave"]) if dados["chave"] else "-"
                            ),
                            "Oferta": (
                                " / ".join(dados["oferta"]) if dados["oferta"] else "-"
                            ),
                        }
                    )

                st.dataframe(
                    dados_tabela,
                    use_container_width=True,
                    hide_index=True,
                )

                # Estatísticas
                st.markdown("---")
                st.subheader("Estatísticas")

                col_stat1, col_stat2, col_stat3 = st.columns(3)

                with col_stat1:
                    total_chaves = sum(
                        1 for d in escala_filtrada if d.funcao == "chave"
                    )
                    st.metric("Total de Chaves", total_chaves)

                with col_stat2:
                    total_ofertas = sum(
                        1 for d in escala_filtrada if d.funcao == "oferta"
                    )
                    st.metric("Total de Ofertas", total_ofertas)

                with col_stat3:
                    diaconos_unicos = len(set(d.nome for d in escala_filtrada))
                    st.metric("Diáconos Envolvidos", diaconos_unicos)

                # Distribuição por diácono
                st.markdown("---")
                st.subheader("Distribuição por Diácono")

                distribuicao = {}
                for diacono in escala_filtrada:
                    if diacono.nome not in distribuicao:
                        distribuicao[diacono.nome] = {"chave": 0, "oferta": 0}
                    distribuicao[diacono.nome][diacono.funcao] += 1

                dados_distribuicao = []
                for nome, contadores in sorted(distribuicao.items()):
                    dados_distribuicao.append(
                        {
                            "Diácono": nome,
                            "Chaves": contadores["chave"],
                            "Ofertas": contadores["oferta"],
                            "Total": contadores["chave"] + contadores["oferta"],
                        }
                    )

                st.dataframe(
                    dados_distribuicao,
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.warning("Nenhum evento encontrado com os filtros selecionados.")

    # Aba 4: Contatos
    with tab4:
        st.header("📞 Contatos")

        st.markdown(
            """
        ### Informações de Contato:
        __Esse aplicativo foi desenvolvido para facilitar a geração
        e gerenciamento de escalas para diáconos com a escala parecida com o da _Igreja Adventista do Sétimo Dia_.__

        Para dúvidas, sugestões ou suporte relacionado ao Gerador de
        Escala para Diáconos, entre em contato através dos canais abaixo.
        """
        )

        col_contato1, col_contato2 = st.columns(2)

        with col_contato1:
            st.subheader("👤 Desenvolvedor")
            st.markdown(
                """
            **Gregório Honorato**

            **Desenvolvedor:**

            📧 Email: greghono@gmail.com

            📱 WhatsApp: [__19 99250-9913__](https://wa.me/5519992509913)

            📱 Telegram: __@greghono__

            📱 LinkedIn: https://www.linkedin.com/in/greghono/

            📱 GitHub: https://github.com/greghonox

            📱 YouTube: [__@greghono__](https://www.youtube.com/@GregorioHonorato)

            """
            )

        with col_contato2:
            st.subheader("ℹ️ Sobre o Aplicativo")
            st.markdown(
                """**Gerador de Escala para Diáconos**

            Versão: 1.0

            **Este aplicativo foi desenvolvido para facilitar a geração
            e gerenciamento de escalas para diáconos.**
            """
            )

        st.markdown("---")

        st.subheader("📝 Sugestões e Melhorias")
        st.info(
            """
        Se você tiver sugestões de melhorias ou encontrar algum problema,
        entre em contato através do telefone informado acima.
        """
        )

        st.markdown("---")

        st.subheader("📚 Documentação")
        st.markdown(
            """
        Para mais informações sobre como usar o aplicativo, consulte:
        - A aba **👥 Diáconos** para gerenciar a lista de diáconos
        - A aba **📅 Escala** para gerar e baixar a escala
        - A aba **📊 Visualização** para análises detalhadas da escala
        """
        )


if __name__ == "__main__":
    main()
