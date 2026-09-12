import streamlit as st
import pandas as pd
import numpy as np

try:
    import altair as alt
except Exception:
    alt = None

st.set_page_config(
    page_title="Previsão de Bandeiras | Energy Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# ENERGY INTELLIGENCE — DARK EDITION
# Interface inspirada no conceito visual aprovado.
# Os dados continuam lendo os Parquets atuais apenas para
# validar a interface. A integração final com Databricks
# será feita depois, sem alterar a identidade visual.
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
  --bg:#061321;
  --panel:#091B2E;
  --panel2:#0C2238;
  --line:#173A58;
  --blue:#087CFF;
  --blue2:#19A7FF;
  --cyan:#00C8FF;
  --orange:#FF7A00;
  --green:#00C878;
  --yellow:#FFC400;
  --red:#FF4050;
  --text:#F5F9FF;
  --muted:#9BB0C5;
  --muted2:#6F8AA3;
}

html, body, [class*="css"] { font-family:Inter, sans-serif; }
.stApp {
  background:
    radial-gradient(circle at 90% 8%, rgba(8,124,255,.12), transparent 28%),
    radial-gradient(circle at 10% 20%, rgba(0,200,255,.05), transparent 25%),
    var(--bg);
  color:var(--text);
}
.block-container { max-width:1280px; padding:1.15rem 1.35rem 3.5rem; }
header[data-testid="stHeader"] { background:transparent; }
footer { visibility:hidden; }

/* topo */
.topbar {
  display:flex; align-items:center; justify-content:space-between; gap:25px;
  padding:4px 2px 20px; border-bottom:1px solid #16344E; margin-bottom:18px;
}
.brand { display:flex; align-items:center; gap:14px; }
.brand-mark {
  width:42px; height:42px; border:1px solid #1D4D73; border-radius:12px;
  display:flex; align-items:center; justify-content:center;
  color:var(--blue2); font-size:24px; background:#071A2B;
  box-shadow:0 0 25px rgba(8,124,255,.16);
}
.brand-name { font-family:'Space Grotesk'; font-size:16px; font-weight:700; letter-spacing:1.5px; }
.brand-sub { color:var(--muted); font-size:11px; margin-top:3px; }
.top-meta { display:flex; align-items:center; gap:28px; color:var(--muted); font-size:11px; }
.top-meta strong { color:#DDEBFA; font-weight:600; }
.meta-sep { height:30px; width:1px; background:#23425D; }

/* navegação */
.stTabs [data-baseweb="tab-list"] {
  background:#071A2A; border:1px solid #153A58; border-radius:12px;
  padding:5px; gap:4px; box-shadow:0 8px 30px rgba(0,0,0,.20);
}
.stTabs [data-baseweb="tab"] {
  color:#9CB1C6; border-radius:9px; padding:9px 15px; font-size:12px; font-weight:600;
}
.stTabs [aria-selected="true"] { background:#075FD0 !important; color:#fff !important; }
.stTabs [data-baseweb="tab-highlight"] { background:transparent !important; }

/* hero */
.hero {
  position:relative; overflow:hidden; min-height:315px; margin-top:20px; padding:42px 42px 36px;
  border:1px solid #164363; border-radius:20px;
  background:
    linear-gradient(90deg, rgba(5,20,34,.98) 0%, rgba(5,24,41,.94) 52%, rgba(5,31,51,.82) 100%);
  box-shadow:0 20px 55px rgba(0,0,0,.28);
}
.hero:after {
  content:'⚡'; position:absolute; right:8%; top:35px; font-size:155px; line-height:1;
  color:rgba(8,124,255,.055); transform:rotate(-10deg); pointer-events:none;
}
.eyebrow { color:#20A8FF; font-size:10px; font-weight:800; letter-spacing:2.3px; text-transform:uppercase; margin-bottom:13px; }
.hero h1 { font-family:'Space Grotesk'; font-size:52px; line-height:.98; letter-spacing:-2px; margin:0; max-width:800px; }
.hero h1 span { color:#087CFF; }
.hero p { color:#C1D0DE; font-size:16px; line-height:1.5; max-width:720px; margin:16px 0 24px; }
.pills { display:flex; flex-wrap:wrap; gap:10px; }
.pill { border:1px solid #27506F; background:#0B263E; border-radius:999px; padding:7px 11px; color:#D7E7F5; font-size:10px; font-weight:700; letter-spacing:.5px; }

/* seção */
.section-head { display:flex; justify-content:space-between; align-items:flex-end; gap:20px; margin:28px 0 14px; }
.section-title { border-left:3px solid var(--blue); padding-left:13px; }
.section-title h2 { font-family:'Space Grotesk'; font-size:20px; margin:0; letter-spacing:.2px; }
.section-title p { color:var(--muted); font-size:12px; margin:5px 0 0; }
.kicker { color:#1598FF; font-size:9px; font-weight:800; letter-spacing:2px; margin-bottom:5px; text-transform:uppercase; }

/* pergunta */
.question {
  margin-top:18px; padding:20px 24px; border:1px solid #0D4F85; border-radius:16px;
  background:#062D55; box-shadow:0 10px 30px rgba(0,0,0,.18);
}
.question-label { color:#55B8FF; font-size:9px; font-weight:800; letter-spacing:2px; text-transform:uppercase; }
.question-text { font-family:'Space Grotesk'; font-size:18px; font-weight:600; margin-top:7px; }

/* cards */
.card-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; }
.card {
  min-height:145px; border:1px solid #19415F; border-radius:15px; background:#091D30;
  padding:20px; position:relative; overflow:hidden; box-shadow:0 10px 25px rgba(0,0,0,.16);
}
.card:before { content:''; position:absolute; top:0; left:0; right:0; height:5px; background:var(--blue); }
.card.green:before { background:var(--green); }
.card.yellow:before { background:var(--yellow); }
.card.red:before { background:var(--red); }
.card.blue:before { background:var(--blue); }
.card-label { color:#A6BAD0; font-size:10px; font-weight:800; letter-spacing:1.4px; text-transform:uppercase; }
.card-value { font-family:'Space Grotesk'; font-size:38px; font-weight:700; margin:17px 0 4px; letter-spacing:-1px; }
.card-note { color:#7F98AF; font-size:11px; line-height:1.4; }
.card-icon { position:absolute; right:18px; bottom:20px; color:#3D78A6; font-size:24px; }

/* impacto */
.impact {
  border:1px solid #173C59; border-radius:16px; background:#081A2C; padding:24px; height:100%;
}
.impact h3 { font-family:'Space Grotesk'; margin:0 0 8px; font-size:18px; }
.impact p { color:#AFC2D3; font-size:13px; line-height:1.55; }
.impact-item { border:1px solid #173C59; background:#0A2034; border-radius:13px; padding:18px; height:100%; }
.impact-icon { font-size:23px; margin-bottom:18px; }
.impact-item h4 { margin:0 0 7px; font-family:'Space Grotesk'; font-size:14px; }
.impact-item p { margin:0; color:#91A8BD; font-size:12px; line-height:1.45; }

/* gráfico / painel */
.chart-card { border:1px solid #173C59; border-radius:16px; background:#081A2C; padding:20px; }
.chart-title { font-family:'Space Grotesk'; font-size:16px; font-weight:700; }
.chart-sub { color:#7892A9; font-size:11px; margin-top:3px; margin-bottom:12px; }
.legend { display:flex; gap:16px; color:#AFC1D2; font-size:10px; margin-top:8px; }
.legend span:before { content:''; display:inline-block; width:9px; height:9px; border-radius:2px; margin-right:5px; background:#00C878; }
.legend .yellow:before { background:#FFC400; }
.legend .red:before { background:#FF4050; }

/* quote */
.quote { margin-top:20px; border:1px solid #173C59; border-radius:16px; background:#07192A; padding:25px 30px; display:flex; gap:22px; align-items:center; }
.quote-mark { color:#087CFF; font-size:54px; line-height:.7; font-weight:800; }
.quote-text { font-family:'Space Grotesk'; font-size:17px; line-height:1.45; color:#E3EDF7; }
.quote-text span { color:#89A4BB; font-family:Inter; font-size:12px; display:block; margin-top:7px; }

.footer-brand { display:flex; justify-content:space-between; margin-top:26px; padding:20px 4px 0; border-top:1px solid #16344E; color:#6F879C; font-size:10px; letter-spacing:.7px; }

/* tabelas e markdown */
.stDataFrame { border:1px solid #173C59; border-radius:12px; overflow:hidden; }
.stMarkdown p, .stMarkdown li { color:#B6C7D6; }
[data-testid="stMetricValue"] { color:#fff; }

@media (max-width:900px) {
  .card-grid { grid-template-columns:repeat(2,1fr); }
  .top-meta { display:none; }
  .hero h1 { font-size:38px; }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DADOS — leitura temporária dos Parquets atuais
# =========================================================
ARQUIVOS = {
    "ENA": "./trusted/ena_mensal.parquet",
    "Bandeiras": "./trusted/bandeira_mensal.parquet",
}

@st.cache_data(show_spinner=False)
def carregar(path):
    try:
        return pd.read_parquet(path)
    except Exception:
        return pd.DataFrame()


def normalizar_mes(df):
    if df.empty:
        return df
    df = df.copy()
    candidatos = ["mes", "Mes", "MesCompetencia", "mes_competencia", "data", "Data"]
    col = next((c for c in candidatos if c in df.columns), None)
    if col:
        df["_mes"] = pd.to_datetime(df[col], errors="coerce")
    return df


df_ena = normalizar_mes(carregar(ARQUIVOS["ENA"]))
df_bandeiras = normalizar_mes(carregar(ARQUIVOS["Bandeiras"]))

# =========================================================
# COMPONENTES
# =========================================================
def risk_card(label, value="—", note="Saída do modelo pendente", tone="blue"):
    return f"""
    <div class="card {tone}">
      <div class="card-label">{label}</div>
      <div class="card-value">{value}</div>
      <div class="card-note">{note}</div>
      <div class="card-icon">▥</div>
    </div>
    """


def section_head(kicker, title, subtitle):
    st.markdown(f"""
    <div class="section-head">
      <div class="section-title">
        <div class="kicker">{kicker}</div>
        <h2>{title}</h2>
        <p>{subtitle}</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# TOPO
# =========================================================
st.markdown("""
<div class="topbar">
  <div class="brand">
    <div class="brand-mark">⌁</div>
    <div>
      <div class="brand-name">ENERGY INTELLIGENCE</div>
      <div class="brand-sub">Dados hoje. Decisões melhores amanhã.</div>
    </div>
  </div>
  <div class="top-meta">
    <div><strong>●</strong>&nbsp;&nbsp; MACKENZIE MBA<br>Engenharia de Dados</div>
    <div class="meta-sep"></div>
    <div><strong>Setor Elétrico Brasileiro</strong><br>Bandeiras Tarifárias</div>
  </div>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs(["⌂  Visão Geral", "▣  Previsão", "⌁  Variáveis", "↗  Histórico", "◉  Modelo", "▣  Metodologia"])

# =========================================================
# VISÃO GERAL
# =========================================================
with tabs[0]:
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">INTELIGÊNCIA PREDITIVA PARA O SETOR ELÉTRICO</div>
      <h1>PREVISÃO DE<br><span>BANDEIRAS TARIFÁRIAS</span></h1>
      <p>Transformando dados climáticos, hidrológicos e do sistema elétrico em sinais antecipados de risco.</p>
      <div class="pills">
        <div class="pill">⚡ ANTECIPAÇÃO DE RISCO</div>
        <div class="pill">▥ DECISÕES MAIS INFORMADAS</div>
        <div class="pill">◈ M+1 · M+2 · M+3</div>
      </div>
    </div>
    <div class="question">
      <div class="question-label">PERGUNTA DE NEGÓCIO</div>
      <div class="question-text">Com as informações disponíveis hoje, conseguimos estimar o risco de bandeira vermelha em M+1, M+2 e M+3?</div>
    </div>
    """, unsafe_allow_html=True)

    section_head("01", "Painel executivo", "A resposta final será apresentada em três horizontes futuros.")
    st.markdown("<div class='card-grid'>" +
        risk_card("BANDEIRA ATUAL", "—", "consulta Databricks na versão final", "green") +
        risk_card("RISCO M+1", "—", "Saída do modelo pendente", "red") +
        risk_card("RISCO M+2", "—", "Saída do modelo pendente", "yellow") +
        risk_card("RISCO M+3", "—", "Saída do modelo pendente", "blue") +
        "</div>", unsafe_allow_html=True)

    section_head("02", "Por que isso importa?", "Antecipar o risco ajuda a transformar informação em planejamento.")
    c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])
    with c1:
        st.markdown("""
        <div class="impact">
          <div class="kicker">VISÃO DE NEGÓCIO</div>
          <h3>A bandeira tarifária impacta diretamente o custo da energia.</h3>
          <p>Antecipar o risco permite interpretar sinais antes da ocorrência observada e apoiar decisões de planejamento, eficiência e resiliência.</p>
        </div>
        """, unsafe_allow_html=True)
    for col, icon, title, text in [
        (c2, "●", "CONSUMIDORES", "Mais previsibilidade no planejamento financeiro."),
        (c3, "▦", "EMPRESAS", "Maior eficiência operacional e redução de riscos."),
        (c4, "◈", "SISTEMA ELÉTRICO", "Contribuição para um setor mais estável e sustentável."),
    ]:
        with col:
            st.markdown(f"""
            <div class="impact-item">
              <div class="impact-icon" style="color:#087CFF">{icon}</div>
              <h4>{title}</h4>
              <p>{text}</p>
            </div>
            """, unsafe_allow_html=True)

    section_head("03", "Evidências no histórico", "Antes de prever o futuro, observamos como o sistema se comportou no passado.")
    a, b = st.columns(2)
    with a:
        st.markdown('<div class="chart-card"><div class="chart-title">Histórico de bandeiras</div><div class="chart-sub">Evolução temporal das bandeiras tarifárias.</div>', unsafe_allow_html=True)
        if not df_bandeiras.empty and "_mes" in df_bandeiras and alt:
            # Escolhe a primeira coluna numérica disponível para uma prévia histórica.
            nums = [c for c in df_bandeiras.columns if c != "_mes" and pd.api.types.is_numeric_dtype(df_bandeiras[c])]
            if nums:
                chart_df = df_bandeiras[["_mes", nums[0]]].dropna().tail(60).rename(columns={nums[0]:"valor"})
                chart = alt.Chart(chart_df).mark_line(strokeWidth=3, color="#00C878").encode(
                    x=alt.X("_mes:T", title=None), y=alt.Y("valor:Q", title=None), tooltip=["_mes:T", "valor:Q"]
                ).properties(height=210).configure_axis(labelColor="#8FA7BD", titleColor="#8FA7BD", gridColor="#17354D")
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("Dados históricos disponíveis, mas sem coluna numérica para exibição.")
        else:
            st.info("A série histórica será alimentada pelo Databricks na versão final.")
        st.markdown('<div class="legend"><span>Verde</span><span class="yellow">Amarela</span><span class="red">Vermelha</span></div></div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="chart-card"><div class="chart-title">Principais variáveis</div><div class="chart-sub">Sinais que ajudam a explicar o comportamento da bandeira.</div>', unsafe_allow_html=True)
        if not df_ena.empty and "_mes" in df_ena and alt:
            nums = [c for c in df_ena.columns if c != "_mes" and pd.api.types.is_numeric_dtype(df_ena[c])]
            if nums:
                cols = nums[:4]
                tmp = df_ena[["_mes"] + cols].dropna(how="all").tail(60)
                long = tmp.melt("_mes", var_name="variavel", value_name="valor").dropna()
                chart = alt.Chart(long).mark_line(strokeWidth=2).encode(
                    x=alt.X("_mes:T", title=None), y=alt.Y("valor:Q", title=None),
                    color=alt.Color("variavel:N", legend=alt.Legend(labelColor="#A8BDCF")),
                    tooltip=["_mes:T", "variavel:N", "valor:Q"]
                ).properties(height=210).configure_axis(labelColor="#8FA7BD", titleColor="#8FA7BD", gridColor="#17354D")
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("Dados disponíveis, mas sem séries numéricas para exibição.")
        else:
            st.info("As variáveis serão visualizadas a partir das camadas do Databricks.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="quote">
      <div class="quote-mark">“</div>
      <div class="quote-text">
        O objetivo não é prever uma certeza.<br>
        É transformar dados disponíveis hoje em um sinal antecipado de risco para os próximos meses.
        <span>DADOS · ANÁLISE · PREVISÃO · DECISÃO</span>
      </div>
    </div>
    <div class="footer-brand">
      <div><strong style="color:#AFC4D7">ENERGY INTELLIGENCE</strong><br>MACKENZIE MBA · ENGENHARIA DE DADOS</div>
      <div>Setor elétrico mais inteligente,<br>decisões mais sustentáveis.</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PREVISÃO
# =========================================================
with tabs[1]:
    section_head("01", "Qual é o risco à frente?", "A previsão transforma as variáveis disponíveis hoje em probabilidade de bandeira vermelha.")
    st.markdown("<div class='card-grid'>" +
        risk_card("M+1 · PRÓXIMO MÊS", "—", "Probabilidade do modelo", "red") +
        risk_card("M+2 · DOIS MESES", "—", "Probabilidade do modelo", "yellow") +
        risk_card("M+3 · TRÊS MESES", "—", "Probabilidade do modelo", "blue") +
        risk_card("ALVO", "RED", "Classificação binária", "red") +
        "</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="question">
      <div class="question-label">INTERPRETAÇÃO</div>
      <div class="question-text">Quanto maior a probabilidade estimada, maior o sinal de atenção para o horizonte analisado.</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# VARIÁVEIS
# =========================================================
with tabs[2]:
    section_head("01", "Os sinais que alimentam a previsão", "Clima, hidrologia e condições do sistema são organizados para a modelagem.")
    cols = st.columns(4)
    itens = [
        ("🌧️", "CLIMA", "Precipitação, acumulado, normal climatológica, temperatura e umidade."),
        ("💧", "HIDROLOGIA", "EAR e ENA representam condições relevantes para o contexto hídrico."),
        ("⚡", "SISTEMA", "CMO e carga ajudam a representar condições de operação e pressão."),
        ("🚦", "HISTÓRICO", "A bandeira observada anteriormente carrega informação temporal."),
    ]
    for col, (icon, title, text) in zip(cols, itens):
        with col:
            st.markdown(f'<div class="impact-item"><div class="impact-icon">{icon}</div><h4>{title}</h4><p>{text}</p></div>', unsafe_allow_html=True)
    section_head("02", "Feature engineering", "O histórico é transformado em sinais temporais para M+1, M+2 e M+3.")
    st.markdown("""
    <div class="chart-card">
      <div class="question-label">FLUXO DE CONSTRUÇÃO</div>
      <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:14px;">
        <div class="pill">DADOS OBSERVADOS</div><div style="color:#087CFF;padding-top:6px;">→</div>
        <div class="pill">LAGS M-1 · M-2</div><div style="color:#087CFF;padding-top:6px;">→</div>
        <div class="pill">VARIAÇÕES</div><div style="color:#087CFF;padding-top:6px;">→</div>
        <div class="pill">MÉDIAS MÓVEIS</div><div style="color:#087CFF;padding-top:6px;">→</div>
        <div class="pill">FEATURES</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# HISTÓRICO
# =========================================================
with tabs[3]:
    section_head("01", "Antes de prever o futuro, olhamos para o passado", "A análise histórica ajuda a identificar padrões, mudanças e relações temporais.")
    if not df_bandeiras.empty:
        st.dataframe(df_bandeiras.tail(24), use_container_width=True, hide_index=True)
    else:
        st.info("A série histórica será carregada da camada Refined do Databricks.")

# =========================================================
# MODELO
# =========================================================
with tabs[4]:
    section_head("01", "Como transformamos sinais em previsão?", "Três horizontes, um objetivo: estimar o risco de bandeira vermelha.")
    st.markdown("""
    <div class="chart-card">
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;align-items:center;text-align:center;">
        <div class="impact-item"><div class="impact-icon">🌧️</div><h4>CLIMA</h4><p>Chuva · temperatura · umidade</p></div>
        <div style="font-size:28px;color:#087CFF;">＋</div>
        <div class="impact-item"><div class="impact-icon">💧</div><h4>HIDROLOGIA</h4><p>EAR · ENA</p></div>
      </div>
      <div style="text-align:center;color:#087CFF;font-size:26px;margin:12px;">↓</div>
      <div class="impact-item" style="text-align:center"><div class="question-label">FEATURE ENGINEERING</div><h4 style="margin-top:8px">Lags · variações · médias</h4></div>
      <div style="text-align:center;color:#087CFF;font-size:26px;margin:12px;">↓</div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;">
        <div class="card red"><div class="card-label">MODELO</div><div class="card-value" style="font-size:26px">M+1</div><div class="card-note">Probabilidade RED</div></div>
        <div class="card yellow"><div class="card-label">MODELO</div><div class="card-value" style="font-size:26px">M+2</div><div class="card-note">Probabilidade RED</div></div>
        <div class="card blue"><div class="card-label">MODELO</div><div class="card-value" style="font-size:26px">M+3</div><div class="card-note">Probabilidade RED</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    section_head("02", "Avaliação", "As métricas reais entram aqui quando o treinamento e o backtest estiverem conectados.")
    st.markdown("<div class='card-grid'>" + risk_card("ROC-AUC", "—", "Pendente", "blue") + risk_card("PRECISÃO", "—", "Pendente", "blue") + risk_card("RECALL", "—", "Pendente", "blue") + risk_card("F1-SCORE", "—", "Pendente", "blue") + "</div>", unsafe_allow_html=True)

# =========================================================
# METODOLOGIA
# =========================================================
with tabs[5]:
    section_head("01", "Da informação à decisão", "Arquitetura do projeto e caminho dos dados até a previsão.")
    st.markdown("""
    <div class="chart-card">
      <div style="display:flex;flex-direction:column;align-items:center;gap:9px;">
        <div class="pill">FONTES · ANEEL · INMET · SISTEMA ELÉTRICO</div><div style="color:#087CFF;font-size:22px">↓</div>
        <div class="pill">RAW</div><div style="color:#087CFF;font-size:22px">↓</div>
        <div class="pill">TRUSTED</div><div style="color:#087CFF;font-size:22px">↓</div>
        <div class="pill">REFINED</div><div style="color:#087CFF;font-size:22px">↓</div>
        <div class="pill">FEATURE ENGINEERING</div><div style="color:#087CFF;font-size:22px">↓</div>
        <div class="pill">MODELO PREDITIVO</div><div style="color:#087CFF;font-size:22px">↓</div>
        <div class="pill" style="border-color:#087CFF;background:#06376A">PROBABILIDADE M+1 · M+2 · M+3</div><div style="color:#087CFF;font-size:22px">↓</div>
        <div class="pill" style="border-color:#00C8FF">STREAMLIT</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="quote">
      <div class="quote-mark">“</div>
      <div class="quote-text">O produto final não entrega uma certeza: entrega um <strong>sinal antecipado de risco</strong> para apoiar decisões sobre o setor elétrico.<span>ENERGY INTELLIGENCE · MACKENZIE MBA · ENGENHARIA DE DADOS</span></div>
    </div>
    """, unsafe_allow_html=True)
