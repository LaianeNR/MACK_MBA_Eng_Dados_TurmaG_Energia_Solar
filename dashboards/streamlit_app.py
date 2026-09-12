import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Previsão de Bandeiras | Energy Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
/* =========================================================
   ENERGY INTELLIGENCE — identidade visual
   Navy + Electric Blue + Cyan
   Verde/Âmbar/Vermelho ficam reservados para status de risco.
   ========================================================= */
.stApp {
    background:
        radial-gradient(circle at 5% 0%, rgba(20,121,255,.12), transparent 25%),
        radial-gradient(circle at 96% 5%, rgba(0,194,255,.10), transparent 24%),
        linear-gradient(180deg, #f7fbff 0%, #eef5fb 55%, #f7fbff 100%);
    color: #071A33;
}
.block-container { max-width: 1480px; padding-top: 1.5rem; padding-bottom: 4rem; }

/* topo */
.hero {
    position: relative;
    overflow: hidden;
    padding: 26px 30px 28px;
    border-radius: 24px;
    margin-bottom: 20px;
    background: linear-gradient(120deg, #071A33 0%, #0b2c52 58%, #075b8f 100%);
    box-shadow: 0 18px 45px rgba(7,26,51,.16);
    border: 1px solid rgba(0,194,255,.20);
}
.hero:after {
    content: "";
    position: absolute;
    width: 360px; height: 360px;
    right: -120px; top: -190px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,194,255,.28), rgba(20,121,255,0) 68%);
}
.hero-topline, .section-number, .info-label, .risk-label {
    color: #63d8ff;
    font-size: 10px;
    font-weight: 850;
    letter-spacing: 1.9px;
    text-transform: uppercase;
}
.hero-title {
    color: #ffffff;
    font-size: 42px;
    font-weight: 900;
    letter-spacing: -2px;
    line-height: 1.02;
    margin-top: 7px;
}
.hero-title span { color: #43c8ff; }
.hero-subtitle { color: #c8e4f7; font-size: 14px; margin-top: 10px; max-width: 950px; }
.hero-badge {
    display: inline-block;
    margin-top: 17px;
    padding: 7px 12px;
    border-radius: 999px;
    background: rgba(255,255,255,.08);
    border: 1px solid rgba(255,255,255,.16);
    color: #e8f7ff;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1px;
}

/* navegação */
.stTabs [data-baseweb="tab-list"] {
    gap: 7px;
    padding: 6px;
    background: rgba(255,255,255,.78);
    border: 1px solid #d8e6f2;
    border-radius: 15px;
    box-shadow: 0 6px 20px rgba(7,26,51,.05);
}
.stTabs [data-baseweb="tab"] {
    color: #607089;
    font-weight: 800;
    border-radius: 10px;
    padding: 9px 13px;
}
.stTabs [aria-selected="true"] {
    color: #071A33 !important;
    background: #e8f4ff;
}

/* seções */
.section { margin-top: 30px; margin-bottom: 17px; padding-left: 15px; border-left: 4px solid #1479FF; }
.section-title { color: #071A33; font-size: 23px; font-weight: 900; letter-spacing: -.5px; }
.section-description { color: #607089; font-size: 13px; margin-top: 5px; }

/* banner */
.banner {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #071A33 0%, #0b3159 62%, #087ca8 100%);
    border-radius: 20px;
    padding: 27px 31px;
    margin: 23px 0;
    box-shadow: 0 14px 38px rgba(7,26,51,.15);
}
.banner:after {
    content: "⚡";
    position: absolute;
    right: 34px; top: 12px;
    font-size: 82px;
    color: rgba(67,200,255,.11);
    transform: rotate(10deg);
}
.banner-label { color: #63d8ff; font-size: 10px; font-weight: 850; letter-spacing: 1.6px; text-transform: uppercase; }
.banner-title { color: #ffffff; font-size: 22px; font-weight: 900; margin-top: 7px; }
.banner-text { color: #d7eaf7; font-size: 13px; line-height: 1.7; max-width: 1030px; margin-top: 9px; }

/* cards */
.kpi, .risk-card, .info-box {
    background: rgba(255,255,255,.97);
    border: 1px solid #d6e4ef;
    border-radius: 18px;
    box-shadow: 0 9px 28px rgba(7,26,51,.065);
}
.kpi { padding: 20px; min-height: 126px; border-top: 3px solid #1479FF; }
.kpi-label { color: #607089; font-size: 10px; font-weight: 850; letter-spacing: 1.1px; margin-bottom: 10px; }
.kpi-value { color: #071A33; font-size: 29px; font-weight: 900; letter-spacing: -1px; }
.kpi-caption { color: #8294a8; font-size: 11px; margin-top: 7px; }
.risk-card { padding: 20px; min-height: 150px; text-align: center; border-top: 3px solid #1479FF; }
.risk-label { color: #607089; }
.risk-value { color: #071A33; font-size: 35px; font-weight: 900; margin-top: 12px; }
.risk-caption { color: #8294a8; font-size: 11px; margin-top: 6px; }
.info-box { padding: 23px; min-height: 175px; }
.info-title { color: #071A33; font-size: 18px; font-weight: 850; margin-bottom: 10px; }
.info-text { color: #607089; font-size: 12px; line-height: 1.75; }

/* destaque visual de status */
.status-strip {
    padding: 13px 16px;
    border-radius: 13px;
    background: #edf7ff;
    border: 1px solid #cce7fb;
    color: #31536f;
    font-size: 12px;
    margin: 15px 0;
}

/* tabelas e componentes */
div[data-testid="stDataFrame"] { border: 1px solid #d6e4ef; border-radius: 14px; overflow: hidden; }
.stAlert { border-radius: 13px; }
.stSelectbox, .stMultiSelect { font-size: 13px; }
.footer { text-align:center; color:#8294a8; font-size:10px; padding-top:50px; letter-spacing:.5px; }

/* botão e links */
a { color: #1479FF !important; }
</style>
""", unsafe_allow_html=True)

# FONTE TEMPORÁRIA: usada para testar o layout.
# Na etapa de integração, será substituída por consultas ao Databricks.
ARQUIVOS = {
    "ENA": "./trusted/ena_mensal.parquet",
    "Bandeiras": "./trusted/bandeira_mensal.parquet",
}

@st.cache_data
def carregar_base(caminho):
    try:
        return pd.read_parquet(caminho)
    except Exception:
        return None

def preparar_data(df):
    if df is None:
        return None
    df = df.copy()
    if "mes" in df.columns:
        df["mes"] = pd.to_datetime(df["mes"].astype(str), errors="coerce")
        df = df.dropna(subset=["mes"]).sort_values("mes").reset_index(drop=True)
    return df

def secao(n, titulo, descricao):
    st.markdown(
        f'<div class="section"><div class="section-number">{n}</div>'
        f'<div class="section-title">{titulo}</div>'
        f'<div class="section-description">{descricao}</div></div>',
        unsafe_allow_html=True,
    )

def banner(label, titulo, texto):
    st.markdown(
        f'<div class="banner"><div class="banner-label">{label}</div>'
        f'<div class="banner-title">{titulo}</div><div class="banner-text">{texto}</div></div>',
        unsafe_allow_html=True,
    )

def kpi(col, titulo, valor, legenda):
    with col:
        st.markdown(
            f'<div class="kpi"><div class="kpi-label">{titulo}</div>'
            f'<div class="kpi-value">{valor}</div><div class="kpi-caption">{legenda}</div></div>',
            unsafe_allow_html=True,
        )

def risco(col, horizonte):
    with col:
        st.markdown(
            f'<div class="risk-card"><div class="risk-label">RISCO {horizonte}</div>'
            f'<div class="risk-value">—</div>'
            f'<div class="risk-caption">Saída do modelo pendente</div></div>',
            unsafe_allow_html=True,
        )

df_ena = preparar_data(carregar_base(ARQUIVOS["ENA"]))
df_bandeiras = preparar_data(carregar_base(ARQUIVOS["Bandeiras"]))

st.markdown(
    '<div class="hero">'
    '<div class="hero-topline">ENERGY INTELLIGENCE • DATA &amp; ELECTRICITY</div>'
    '<div class="hero-title">⚡ PREVISÃO DE <span>BANDEIRAS</span></div>'
    '<div class="hero-subtitle">Inteligência preditiva aplicada à antecipação do risco tarifário no setor elétrico brasileiro</div>'
    '<div class="hero-badge">M+1 &nbsp;•&nbsp; M+2 &nbsp;•&nbsp; M+3 &nbsp; | &nbsp; RISCO TARIFÁRIO</div>'
    '</div>',
    unsafe_allow_html=True,
)

tab_visao, tab_prev, tab_vars, tab_hist, tab_modelo, tab_met = st.tabs([
    "🔎 Visão Geral", "🤖 Previsão", "🌧️ Variáveis", "📈 Histórico", "🧠 Modelo", "📚 Metodologia"
])

with tab_visao:
    banner(
        "01 / VISÃO EXECUTIVA",
        "⚡ ANTECIPAÇÃO DO RISCO TARIFÁRIO",
        "Transformamos dados climáticos, hidrológicos e do sistema elétrico em inteligência para antecipar a probabilidade de bandeira vermelha nos horizontes M+1, M+2 e M+3."
    )
    secao("01", "Painel executivo", "Resumo do estado atual e dos horizontes de previsão.")
    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "BANDEIRA ATUAL", "—", "consulta Databricks na versão final")
    risco(c2, "M+1")
    risco(c3, "M+2")
    risco(c4, "M+3")

    secao("02", "O problema em foco", "Qual pergunta o modelo pretende responder?")
    a, b = st.columns(2)
    with a:
        st.markdown(
            '<div class="info-box"><div class="info-label">TARGET</div>'
            '<div class="info-title">Bandeira vermelha</div>'
            '<div class="info-text">A previsão é tratada como classificação binária: <b>1 = bandeira vermelha</b> e <b>0 = demais situações</b>.<br><br>O resultado final será uma <b>probabilidade</b>, e não uma certeza.</div></div>',
            unsafe_allow_html=True,
        )
    with b:
        st.markdown(
            '<div class="info-box"><div class="info-label">HORIZONTES</div>'
            '<div class="info-title">M+1 • M+2 • M+3</div>'
            '<div class="info-text">A solução estima o risco para o próximo mês, dois meses à frente e três meses à frente.<br><br>Isso permite comparar como o risco muda conforme aumenta o horizonte.</div></div>',
            unsafe_allow_html=True,
        )

with tab_prev:
    banner(
        "02 / MODELO PREDITIVO",
        "🤖 PROBABILIDADE DE BANDEIRA VERMELHA",
        "O produto final será uma leitura objetiva do risco: qual a probabilidade estimada de bandeira vermelha em cada horizonte?"
    )
    secao("01", "Três horizontes, uma decisão", "Probabilidade estimada para cada janela futura.")
    c1, c2, c3 = st.columns(3)
    risco(c1, "M+1")
    risco(c2, "M+2")
    risco(c3, "M+3")
    st.markdown('<div class="status-strip">🔵 <b>Status da versão:</b> interface preparada. Os percentuais serão preenchidos somente após a integração com a saída real do modelo.</div>', unsafe_allow_html=True)
    secao("02", "Como interpretar", "A probabilidade é uma estimativa produzida pelo modelo a partir das variáveis disponíveis.")
    st.markdown("Se o modelo apresentar **70% para M+1**, isso significa que, dadas as informações utilizadas pelo modelo, a probabilidade estimada de ocorrência de bandeira vermelha no próximo mês é de 70%. Isso não representa certeza nem causalidade.")

with tab_vars:
    banner(
        "03 / VARIÁVEIS EXPLICATIVAS",
        "🌧️ O QUE ESTÁ ASSOCIADO AO RISCO?",
        "Clima, hidrologia e condições do sistema elétrico formam o conjunto de sinais analisados pela solução preditiva."
    )
    secao("01", "Indicadores disponíveis", "Explore a série histórica disponível nesta versão de demonstração.")
    if df_ena is not None and not df_ena.empty:
        cols = [c for c in df_ena.columns if c != "mes" and pd.api.types.is_numeric_dtype(df_ena[c])]
        if cols:
            sel = st.multiselect("Selecione os indicadores", cols, default=cols[:min(3, len(cols))], key="vars")
            if sel:
                st.line_chart(df_ena[["mes"] + sel].set_index("mes"), use_container_width=True)
        else:
            st.info("A base atual não possui indicadores numéricos disponíveis.")
    else:
        st.warning("Base ENA não disponível nesta versão temporária.")

    secao("02", "Variáveis do modelo", "Conjunto de sinais previsto para a análise final no Databricks.")
    x, y, z = st.columns(3)
    with x:
        st.markdown('<div class="info-box"><div class="info-label">CLIMA</div><div class="info-title">🌧️ Chuva & atmosfera</div><div class="info-text">Precipitação média, acumulada, % da normal, temperatura e umidade.</div></div>', unsafe_allow_html=True)
    with y:
        st.markdown('<div class="info-box"><div class="info-label">HIDROLOGIA</div><div class="info-title">💧 Reservatórios & afluências</div><div class="info-text">EAR e ENA, incluindo histórico e variações quando disponíveis.</div></div>', unsafe_allow_html=True)
    with z:
        st.markdown('<div class="info-box"><div class="info-label">SISTEMA</div><div class="info-title">⚡ Demanda & custo</div><div class="info-text">CMO, carga e histórico de bandeiras como sinais do sistema.</div></div>', unsafe_allow_html=True)

with tab_hist:
    banner(
        "04 / SÉRIE HISTÓRICA",
        "📈 O COMPORTAMENTO AO LONGO DO TEMPO",
        "A visão histórica ajuda a contextualizar as mudanças de bandeira e a relação temporal com os indicadores do sistema."
    )
    if df_bandeiras is None or df_bandeiras.empty:
        st.warning("Base histórica de bandeiras não disponível.")
    else:
        secao("01", "Histórico das bandeiras", "Evolução temporal dos registros disponíveis.")
        candidatos = [c for c in ["NivelBandeira", "nivel_bandeira", "VlrAdicionalBandeira", "ValorAdicionalBandeira"] if c in df_bandeiras.columns]
        if candidatos:
            v = candidatos[0]
            dados = df_bandeiras[["mes", v]].copy()
            dados[v] = pd.to_numeric(dados[v], errors="coerce")
            st.line_chart(dados.dropna().set_index("mes")[v], use_container_width=True)
        st.dataframe(df_bandeiras.tail(12), use_container_width=True, hide_index=True)

with tab_modelo:
    banner(
        "05 / AVALIAÇÃO PREDITIVA",
        "🧠 MODELO, BACKTEST E PERFORMANCE",
        "Aqui serão apresentados os resultados do treinamento e da validação cronológica para os três horizontes de previsão."
    )
    secao("01", "Horizontes avaliados", "Cada horizonte possui um alvo específico de previsão.")
    st.dataframe(
        pd.DataFrame({
            "Horizonte": ["M+1", "M+2", "M+3"],
            "Alvo": ["Bandeira vermelha no mês seguinte", "Bandeira vermelha em dois meses", "Bandeira vermelha em três meses"],
            "Status": ["Aguardando modelo"] * 3,
        }),
        use_container_width=True,
        hide_index=True,
    )
    secao("02", "Métricas", "Os valores reais serão preenchidos após a validação dos modelos.")
    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "ACURÁCIA", "—", "resultado do backtest")
    kpi(c2, "PRECISÃO", "—", "classe vermelha")
    kpi(c3, "RECALL", "—", "classe vermelha")
    kpi(c4, "F1 / ROC-AUC", "—", "avaliação do modelo")

with tab_met:
    banner(
        "06 / ARQUITETURA DE DADOS",
        "📚 DA FONTE À PROBABILIDADE",
        "O dashboard representa a camada de consumo da solução, conectando a arquitetura de dados ao resultado preditivo."
    )
    secao("01", "Fluxo da solução", "Arquitetura conceitual do projeto.")
    st.code("""Fontes de dados
        ↓
Camada Raw
        ↓
Camada Trusted
        ↓
Camada Refined
        ↓
Feature Engineering
        ↓
Modelo Preditivo
        ↓
Probabilidade M+1 / M+2 / M+3
        ↓
Dashboard Streamlit""", language="text")
    secao("02", "Camada visual", "Integração planejada com a plataforma de dados.")
    st.markdown("**Arquitetura planejada:** `Databricks → SQL Warehouse → Streamlit`\n\nO dashboard apresenta indicadores, histórico e resultados produzidos pelas camadas de dados e pelo modelo.")
    secao("03", "Escopo da previsão", "Objetivo da aplicação.")
    st.markdown("O foco é antecipar o risco de ocorrência de **bandeira tarifária vermelha** nos horizontes **M+1, M+2 e M+3**, utilizando variáveis climáticas, hidrológicas e energéticas disponíveis no projeto.")

st.markdown('<div class="footer">ENERGY INTELLIGENCE • PREVISÃO DE BANDEIRAS • MBA EM ENGENHARIA DE DADOS</div>', unsafe_allow_html=True)
