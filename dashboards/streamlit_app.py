
import os
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Previsão de Bandeiras | Energy Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# ENERGY INTELLIGENCE — DARK EXECUTIVE DASHBOARD
# Layout intentionally mirrors the approved visual reference.
# No real prediction probabilities are fabricated.
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #061522;
        --bg-2: #081d2e;
        --panel: #0a2133;
        --panel-2: #0c273b;
        --line: #16405d;
        --line-soft: #12334b;
        --white: #f4f8fc;
        --muted: #8fa8bb;
        --blue: #087cff;
        --blue-2: #16a0ff;
        --green: #00b86b;
        --yellow: #ffc400;
        --red: #ff3b4e;
        --orange: #ff7a00;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 85% 8%, rgba(8,124,255,.08), transparent 28%),
            radial-gradient(circle at 8% 35%, rgba(0,184,107,.035), transparent 25%),
            var(--bg);
        color: var(--white);
    }

    .main .block-container {
        max-width: 1180px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stToolbar"] {
        background: transparent;
    }

    /* Top brand */
    .brandbar {
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap:30px;
        padding: 4px 2px 20px 2px;
        border-bottom: 1px solid var(--line-soft);
    }

    .brand-left {
        display:flex;
        align-items:center;
        gap:14px;
    }

    .brand-mark {
        width:42px;
        height:42px;
        border:1px solid #1b6da4;
        border-radius:11px;
        display:flex;
        align-items:center;
        justify-content:center;
        color:var(--blue-2);
        font-size:24px;
        font-weight:800;
        background:#071b2b;
    }

    .brand-name {
        font-size:18px;
        font-weight:800;
        letter-spacing:.4px;
        color:#f6fbff;
    }

    .brand-sub {
        margin-top:2px;
        color:#87a2b6;
        font-size:10px;
        letter-spacing:.2px;
    }

    .brand-meta {
        display:flex;
        align-items:center;
        gap:28px;
        color:#b5c7d5;
        font-size:11px;
        text-align:left;
    }

    .brand-meta-item {
        padding-left:20px;
        border-left:1px solid #1a3b53;
        line-height:1.45;
    }

    .brand-meta-dot {
        color:var(--blue);
        font-size:16px;
        vertical-align:middle;
        margin-right:7px;
    }

    /* Hero */
    .hero {
        position:relative;
        overflow:hidden;
        min-height:320px;
        margin-top:26px;
        padding:42px 38px 34px 38px;
        border:1px solid #145077;
        border-radius:18px;
        background:
            linear-gradient(90deg, rgba(6,21,34,.99) 0%, rgba(7,28,45,.96) 57%, rgba(5,30,48,.86) 100%);
        box-shadow:0 18px 50px rgba(0,0,0,.22);
    }

    .hero::after {
        content:"";
        position:absolute;
        inset:0;
        pointer-events:none;
        background:
            linear-gradient(90deg, transparent 62%, rgba(8,124,255,.04)),
            repeating-linear-gradient(120deg, transparent 0 80px, rgba(33,105,145,.025) 80px 81px);
    }

    .hero-kicker {
        position:relative;
        z-index:2;
        color:#1595ff;
        font-size:11px;
        font-weight:800;
        letter-spacing:2.2px;
        text-transform:uppercase;
        margin-bottom:12px;
    }

    .hero-title {
        position:relative;
        z-index:2;
        margin:0;
        max-width:760px;
        font-size:48px;
        line-height:1.02;
        font-weight:800;
        letter-spacing:-1.7px;
        color:#f5f8fb;
    }

    .hero-title .accent {
        color:#087cff;
    }

    .hero-sub {
        position:relative;
        z-index:2;
        max-width:690px;
        margin-top:15px;
        color:#bfd0dc;
        font-size:16px;
        line-height:1.5;
    }

    .hero-benefits {
        position:relative;
        z-index:2;
        display:flex;
        gap:28px;
        margin-top:28px;
        flex-wrap:wrap;
    }

    .benefit {
        display:flex;
        align-items:center;
        gap:10px;
        color:#dce8f0;
        font-size:13px;
        line-height:1.35;
        padding-right:26px;
        border-right:1px solid #15374e;
    }

    .benefit:last-child { border-right:0; }

    .benefit-icon {
        width:31px;
        height:31px;
        border-radius:50%;
        display:flex;
        align-items:center;
        justify-content:center;
        background:#087cff;
        color:white;
        font-size:16px;
        flex:0 0 auto;
    }

    .hero-side {
        position:absolute;
        right:36px;
        top:100px;
        width:150px;
        z-index:2;
        border-left:2px solid #0d8dff;
        padding-left:16px;
        color:#9eb4c4;
        font-size:11px;
        line-height:1.75;
        letter-spacing:3px;
        text-transform:uppercase;
    }

    /* Business question */
    .question {
        display:flex;
        align-items:center;
        gap:24px;
        margin-top:20px;
        padding:23px 25px;
        border:1px solid #154563;
        border-radius:15px;
        background:#071c2c;
    }

    .question-bar {
        width:7px;
        min-height:64px;
        border-radius:7px;
        background:#087cff;
        flex:0 0 auto;
    }

    .eyebrow {
        color:#1195ff;
        font-size:9px;
        font-weight:800;
        letter-spacing:2px;
        text-transform:uppercase;
    }

    .question-text {
        margin-top:6px;
        color:#f1f6fa;
        font-size:17px;
        line-height:1.4;
        font-weight:700;
    }

    .question-action {
        margin-left:auto;
        min-width:130px;
        padding-left:24px;
        border-left:1px solid #1a415b;
        color:#e3edf4;
        font-size:12px;
        line-height:1.4;
    }

    .question-action span {
        color:#087cff;
        font-size:28px;
        vertical-align:middle;
        margin-right:8px;
    }

    /* Section */
    .section-head {
        display:flex;
        justify-content:space-between;
        align-items:flex-end;
        margin-top:27px;
        margin-bottom:13px;
    }

    .section-title {
        border-left:4px solid #087cff;
        padding-left:16px;
    }

    .section-title h2 {
        margin:0;
        color:#eef5fa;
        font-size:17px;
        font-weight:800;
        letter-spacing:.3px;
        text-transform:uppercase;
    }

    .section-title p {
        margin:5px 0 0;
        color:#829bad;
        font-size:11px;
    }

    .update {
        color:#93aabb;
        font-size:11px;
        text-align:right;
    }

    /* Cards */
    .cards {
        display:grid;
        grid-template-columns:repeat(4, 1fr);
        gap:14px;
    }

    .risk-card {
        position:relative;
        min-height:155px;
        overflow:hidden;
        border:1px solid #19425b;
        border-radius:14px;
        background:linear-gradient(180deg, #0b2639 0%, #081d2e 100%);
        box-shadow:0 10px 25px rgba(0,0,0,.14);
    }

    .risk-card::before {
        content:"";
        display:block;
        height:6px;
        background:var(--card-color);
    }

    .risk-inner {
        padding:19px 20px 17px;
    }

    .risk-label {
        color:#dce8ef;
        font-size:11px;
        font-weight:800;
        letter-spacing:1.3px;
        text-transform:uppercase;
    }

    .risk-value {
        margin-top:30px;
        color:#f6fbff;
        font-size:30px;
        line-height:1;
        font-weight:800;
    }

    .risk-note {
        margin-top:12px;
        color:#8da7b8;
        font-size:11px;
        line-height:1.4;
    }

    .risk-icon {
        position:absolute;
        right:18px;
        bottom:18px;
        color:#6b92ae;
        font-size:25px;
    }

    /* Impact */
    .impact {
        display:grid;
        grid-template-columns:1.05fr 2fr;
        gap:18px;
        margin-top:18px;
        padding:25px;
        border:1px solid #16405a;
        border-radius:15px;
        background:#071c2c;
    }

    .impact-intro h3 {
        margin:7px 0 10px;
        color:#f4f8fb;
        font-size:21px;
        line-height:1.18;
    }

    .impact-intro p {
        margin:0;
        color:#a8bccb;
        font-size:12px;
        line-height:1.65;
        max-width:330px;
    }

    .impact-button {
        display:inline-block;
        margin-top:17px;
        padding:9px 15px;
        border-radius:7px;
        background:#087cff;
        color:white;
        font-size:11px;
        font-weight:700;
    }

    .impact-grid {
        display:grid;
        grid-template-columns:repeat(3,1fr);
        gap:12px;
    }

    .impact-card {
        min-height:150px;
        padding:18px;
        border:1px solid #19435c;
        border-radius:12px;
        background:#092337;
    }

    .impact-icon {
        color:#087cff;
        font-size:22px;
    }

    .impact-card h4 {
        margin:19px 0 8px;
        color:#f2f7fa;
        font-size:12px;
        letter-spacing:.5px;
    }

    .impact-card p {
        margin:0;
        color:#92aabb;
        font-size:11px;
        line-height:1.55;
    }

    /* Evidence cards */
    .evidence-grid {
        display:grid;
        grid-template-columns:1fr 1fr;
        gap:18px;
    }

    .chart-card {
        min-height:290px;
        padding:20px;
        border:1px solid #16405a;
        border-radius:15px;
        background:#071c2c;
    }

    .chart-title {
        color:#edf4f8;
        font-size:14px;
        font-weight:800;
    }

    .chart-sub {
        margin-top:4px;
        color:#819bad;
        font-size:10px;
    }

    .chart-placeholder {
        height:185px;
        margin-top:18px;
        border-radius:9px;
        border:1px dashed #214a63;
        display:flex;
        align-items:center;
        justify-content:center;
        color:#5f7f95;
        font-size:11px;
        background:
            repeating-linear-gradient(0deg, transparent 0 35px, rgba(42,86,112,.14) 35px 36px);
    }

    .legend {
        display:flex;
        gap:16px;
        margin-top:12px;
        color:#93aabb;
        font-size:10px;
    }

    .dot {
        display:inline-block;
        width:8px;
        height:8px;
        border-radius:2px;
        margin-right:5px;
    }

    /* Closing */
    .closing {
        display:flex;
        align-items:center;
        gap:22px;
        margin-top:18px;
        padding:25px;
        border:1px solid #16405a;
        border-radius:15px;
        background:#071c2c;
    }

    .quote {
        color:#087cff;
        font-size:45px;
        font-weight:800;
        line-height:1;
    }

    .closing-text {
        color:#e7eef3;
        font-size:14px;
        line-height:1.55;
        font-weight:600;
    }

    .closing-text small {
        display:block;
        margin-top:5px;
        color:#718da2;
        font-size:10px;
        font-weight:400;
    }

    .closing-side {
        margin-left:auto;
        padding-left:25px;
        border-left:1px solid #1a415a;
        color:#7893a6;
        font-size:9px;
        line-height:1.8;
        letter-spacing:2px;
        text-transform:uppercase;
    }

    .footer {
        display:flex;
        justify-content:space-between;
        margin-top:30px;
        padding:0 3px;
        color:#5f7d91;
        font-size:9px;
        letter-spacing:1px;
        text-transform:uppercase;
    }

    /* Streamlit tabs */
    div[data-baseweb="tab-list"] {
        gap:4px;
        background:transparent;
        border-bottom:1px solid #153b54;
        margin-top:12px;
    }

    button[data-baseweb="tab"] {
        color:#7793a7 !important;
        background:transparent !important;
        border-radius:7px 7px 0 0 !important;
        padding:10px 15px !important;
        font-size:11px !important;
        font-weight:600 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color:#ffffff !important;
        background:#087cff !important;
    }

    div[data-baseweb="tab-highlight"] {
        display:none !important;
    }

    /* Native Streamlit text inside dark theme */
    .stMarkdown, .stText, label, p {
        color:inherit;
    }

    @media (max-width: 900px) {
        .hero-title { font-size:36px; }
        .hero-side { display:none; }
        .cards { grid-template-columns:repeat(2,1fr); }
        .impact, .evidence-grid { grid-template-columns:1fr; }
        .brand-meta { display:none; }
    }

    @media (max-width: 600px) {
        .cards { grid-template-columns:1fr; }
        .impact-grid { grid-template-columns:1fr; }
        .hero { padding:28px 22px; }
        .question-action { display:none; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def find_parquet(filename: str):
    candidates = [
        Path("trusted") / filename,
        Path("refined") / filename,
        Path("datasets") / filename,
        Path(filename),
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def load_optional_bandeiras():
    names = [
        "bandeira_mensal.parquet",
        "bandeiras_mensal.parquet",
        "painel_mensal_bandeira_hidrologia.parquet",
    ]
    for name in names:
        path = find_parquet(name)
        if path:
            try:
                return pd.read_parquet(path)
            except Exception:
                pass
    return None


def load_optional_model():
    names = [
        "modelo_previsao_bandeira.parquet",
        "f_modelo_bandeira_clima.parquet",
    ]
    for name in names:
        path = find_parquet(name)
        if path:
            try:
                return pd.read_parquet(path)
            except Exception:
                pass
    return None


def html_cards():
    return """
    <div class="cards">
      <div class="risk-card" style="--card-color:#00b86b;">
        <div class="risk-inner">
          <div class="risk-label">Bandeira atual</div>
          <div class="risk-value">—</div>
          <div class="risk-note">consulta Databricks na versão final</div>
        </div>
        <div class="risk-icon">⚑</div>
      </div>

      <div class="risk-card" style="--card-color:#ff3b4e;">
        <div class="risk-inner">
          <div class="risk-label">Risco M+1</div>
          <div class="risk-value">—</div>
          <div class="risk-note">Saída do modelo pendente</div>
        </div>
        <div class="risk-icon">▥</div>
      </div>

      <div class="risk-card" style="--card-color:#ffc400;">
        <div class="risk-inner">
          <div class="risk-label">Risco M+2</div>
          <div class="risk-value">—</div>
          <div class="risk-note">Saída do modelo pendente</div>
        </div>
        <div class="risk-icon">▥</div>
      </div>

      <div class="risk-card" style="--card-color:#087cff;">
        <div class="risk-inner">
          <div class="risk-label">Risco M+3</div>
          <div class="risk-value">—</div>
          <div class="risk-note">Saída do modelo pendente</div>
        </div>
        <div class="risk-icon">▥</div>
      </div>
    </div>
    """


def impact_section():
    return """
    <div class="impact">
      <div class="impact-intro">
        <div class="eyebrow">Por que isso importa?</div>
        <h3>A bandeira tarifária impacta diretamente o custo da energia.</h3>
        <p>
          Antecipar o risco permite transformar informação em planejamento,
          eficiência e maior resiliência para o setor elétrico.
        </p>
        <div class="impact-button">Entenda o problema&nbsp; →</div>
      </div>

      <div class="impact-grid">
        <div class="impact-card">
          <div class="impact-icon">●</div>
          <h4>CONSUMIDORES</h4>
          <p>Mais previsibilidade no planejamento financeiro.</p>
        </div>
        <div class="impact-card">
          <div class="impact-icon">▣</div>
          <h4>EMPRESAS</h4>
          <p>Maior eficiência operacional e redução de riscos.</p>
        </div>
        <div class="impact-card">
          <div class="impact-icon">◆</div>
          <h4>SISTEMA ELÉTRICO</h4>
          <p>Contribuição para um setor mais estável e sustentável.</p>
        </div>
      </div>
    </div>
    """


def closing_section():
    return """
    <div class="closing">
      <div class="quote">“</div>
      <div class="closing-text">
        O objetivo não é prever uma certeza.<br>
        É transformar dados disponíveis hoje em um sinal antecipado de risco para os próximos meses.
        <small>DADOS · ANÁLISE · PREVISÃO · DECISÃO</small>
      </div>
      <div class="closing-side">
        Dados<br>
        Análise<br>
        Previsão<br>
        Decisão
      </div>
    </div>

    <div class="footer">
      <div>Energy Intelligence · Mackenzie MBA · Engenharia de Dados</div>
      <div>Setor elétrico mais inteligente, decisões mais sustentáveis.</div>
    </div>
    """


# ------------------------------------------------------------
# Header
# ------------------------------------------------------------

st.markdown(
    """
    <div class="brandbar">
      <div class="brand-left">
        <div class="brand-mark">⌁</div>
        <div>
          <div class="brand-name">ENERGY INTELLIGENCE</div>
          <div class="brand-sub">Dados hoje. Decisões melhores amanhã.</div>
        </div>
      </div>

      <div class="brand-meta">
        <div class="brand-meta-item">
          <span class="brand-meta-dot">●</span>
          MACKENZIE MBA<br>
          Engenharia de Dados
        </div>
        <div class="brand-meta-item">
          Setor Elétrico Brasileiro<br>
          Bandeiras Tarifárias
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

tabs = st.tabs(
    [
        "⌂  Visão Geral",
        "▣  Previsão",
        "⌁  Variáveis",
        "↗  Histórico",
        "●  Modelo",
        "▣  Metodologia",
    ]
)

# ------------------------------------------------------------
# TAB 1 — Visão Geral
# ------------------------------------------------------------

with tabs[0]:
    st.markdown(
        """
        <div class="hero">
          <div class="hero-kicker">Inteligência preditiva para o setor elétrico</div>
          <h1 class="hero-title">
            PREVISÃO DE<br>
            <span class="accent">BANDEIRAS TARIFÁRIAS</span>
          </h1>
          <div class="hero-sub">
            Transformando dados climáticos, hidrológicos e do sistema elétrico
            em sinais antecipados de risco.
          </div>

          <div class="hero-benefits">
            <div class="benefit">
              <span class="benefit-icon">⚡</span>
              Antecipação<br>de risco
            </div>
            <div class="benefit">
              <span class="benefit-icon">▥</span>
              Decisões<br>mais informadas
            </div>
            <div class="benefit">
              <span class="benefit-icon">◆</span>
              Contribuição para um<br>setor elétrico mais estável
            </div>
          </div>

          <div class="hero-side">
            ENERGIA<br>
            DADOS<br>
            PESSOAS<br>
            UM FUTURO<br>
            MAIS ESTÁVEL
          </div>
        </div>

        <div class="question">
          <div class="question-bar"></div>
          <div>
            <div class="eyebrow">Pergunta de negócio</div>
            <div class="question-text">
              Com as informações disponíveis hoje, conseguimos estimar o risco
              de bandeira vermelha em M+1, M+2 e M+3?
            </div>
          </div>
          <div class="question-action">
            <span>›</span> Explorar<br>previsões
          </div>
        </div>

        <div class="section-head">
          <div class="section-title">
            <h2>Painel executivo</h2>
            <p>A resposta final será apresentada em três horizontes futuros.</p>
          </div>
          <div class="update">Última atualização<br><strong>—</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(html_cards(), unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-head">
          <div class="section-title">
            <h2>Por que isso importa?</h2>
            <p>O valor do modelo está em antecipar um sinal de risco antes da decisão.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(impact_section(), unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-head">
          <div class="section-title">
            <h2>Evidências no histórico</h2>
            <p>Antes de prever o futuro, observamos o comportamento histórico dos indicadores.</p>
          </div>
        </div>

        <div class="evidence-grid">
          <div class="chart-card">
            <div class="chart-title">Histórico de bandeiras</div>
            <div class="chart-sub">Evolução das bandeiras tarifárias ao longo do tempo.</div>
        """,
        unsafe_allow_html=True,
    )

    # Native chart area — deliberately separated from the HTML shell
    bandeiras = load_optional_bandeiras()
    if bandeiras is not None and len(bandeiras) > 0:
        st.info("Base histórica encontrada. A visualização definitiva será ligada ao Databricks.")
    else:
        st.markdown(
            '<div class="chart-placeholder">Histórico será alimentado pelo Databricks</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        """
          </div>
          <div class="chart-card">
            <div class="chart-title">Principais variáveis</div>
            <div class="chart-sub">Sinais que ajudam a explicar o comportamento da bandeira.</div>
        """,
        unsafe_allow_html=True,
    )

    modelo = load_optional_model()
    if modelo is not None and len(modelo) > 0:
        st.info("Variáveis encontradas. A visualização definitiva será ligada ao Databricks.")
    else:
        st.markdown(
            '<div class="chart-placeholder">ENA · EAR · CMO · Carga · Chuva</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        """
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(closing_section(), unsafe_allow_html=True)


# ------------------------------------------------------------
# TAB 2 — Previsão
# ------------------------------------------------------------

with tabs[1]:
    st.markdown(
        """
        <div class="section-head">
          <div class="section-title">
            <h2>Qual é o risco à frente?</h2>
            <p>A previsão transforma as variáveis disponíveis hoje em probabilidade de bandeira vermelha.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="cards">
          <div class="risk-card" style="--card-color:#ff3b4e;">
            <div class="risk-inner">
              <div class="risk-label">M+1 · Próximo mês</div>
              <div class="risk-value">—</div>
              <div class="risk-note">Probabilidade do modelo</div>
            </div>
            <div class="risk-icon">▥</div>
          </div>
          <div class="risk-card" style="--card-color:#ffc400;">
            <div class="risk-inner">
              <div class="risk-label">M+2 · Dois meses</div>
              <div class="risk-value">—</div>
              <div class="risk-note">Probabilidade do modelo</div>
            </div>
            <div class="risk-icon">▥</div>
          </div>
          <div class="risk-card" style="--card-color:#087cff;">
            <div class="risk-inner">
              <div class="risk-label">M+3 · Três meses</div>
              <div class="risk-value">—</div>
              <div class="risk-note">Probabilidade do modelo</div>
            </div>
            <div class="risk-icon">▥</div>
          </div>
          <div class="risk-card" style="--card-color:#087cff;">
            <div class="risk-inner">
              <div class="risk-label">Classe-alvo</div>
              <div class="risk-value" style="font-size:24px;">VERMELHA</div>
              <div class="risk-note">Classificação binária</div>
            </div>
            <div class="risk-icon">●</div>
          </div>
        </div>

        <div class="question" style="margin-top:18px;">
          <div class="question-bar"></div>
          <div>
            <div class="eyebrow">Interpretação</div>
            <div class="question-text" style="font-size:14px;">
              Quanto maior a probabilidade estimada, maior o sinal de atenção para o horizonte analisado.
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# TAB 3 — Variáveis
# ------------------------------------------------------------

with tabs[2]:
    st.markdown(
        """
        <div class="section-head">
          <div class="section-title">
            <h2>Quais sinais entram na previsão?</h2>
            <p>As variáveis representam clima, hidrologia, sistema elétrico e histórico.</p>
          </div>
        </div>

        <div class="impact">
          <div class="impact-intro">
            <div class="eyebrow">Sinais do modelo</div>
            <h3>Dados disponíveis hoje para olhar o risco de amanhã.</h3>
            <p>
              O projeto combina variáveis observadas e transformações temporais
              para construir as features usadas na classificação.
            </p>
          </div>
          <div class="impact-grid">
            <div class="impact-card">
              <div class="impact-icon">≈</div>
              <h4>CLIMA</h4>
              <p>Precipitação, acumulado, normal climatológica, temperatura e umidade.</p>
            </div>
            <div class="impact-card">
              <div class="impact-icon">◆</div>
              <h4>HIDROLOGIA</h4>
              <p>EAR, ENA e suas variações temporais.</p>
            </div>
            <div class="impact-card">
              <div class="impact-icon">⚡</div>
              <h4>SISTEMA ELÉTRICO</h4>
              <p>CMO, carga e histórico de bandeira.</p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-head">
          <div class="section-title">
            <h2>Feature engineering</h2>
            <p>Lags, variações e médias ajudam a representar o comportamento temporal.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df_model = load_optional_model()
    if df_model is not None and len(df_model):
        cols = [
            c for c in [
                "EAR_M0", "EAR_M1", "EAR_M2",
                "ENA_M0", "ENA_M1", "ENA_M2",
                "ChuvaMedia_M0", "ChuvaMedia_M1", "ChuvaMedia_M2",
                "Temperatura_M0", "Umidade_M0"
            ] if c in df_model.columns
        ]
        if cols:
            st.dataframe(
                df_model[cols].head(10),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("A tabela de features será exibida após a conexão final com o Databricks.")
    else:
        st.markdown(
            '<div class="chart-placeholder">Tabela de features · Databricks</div>',
            unsafe_allow_html=True,
        )


# ------------------------------------------------------------
# TAB 4 — Histórico
# ------------------------------------------------------------

with tabs[3]:
    st.markdown(
        """
        <div class="section-head">
          <div class="section-title">
            <h2>Antes de prever o futuro, olhamos o passado</h2>
            <p>Evolução temporal das bandeiras e dos principais indicadores.</p>
          </div>
        </div>

        <div class="evidence-grid">
          <div class="chart-card">
            <div class="chart-title">Bandeiras ao longo do tempo</div>
            <div class="chart-sub">Verde · Amarela · Vermelha</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
            <div class="chart-placeholder">Gráfico histórico será alimentado pelo Databricks</div>
            <div class="legend">
              <span><i class="dot" style="background:#00b86b;"></i>Verde</span>
              <span><i class="dot" style="background:#ffc400;"></i>Amarela</span>
              <span><i class="dot" style="background:#ff3b4e;"></i>Vermelha</span>
            </div>
          </div>

          <div class="chart-card">
            <div class="chart-title">Variáveis no tempo</div>
            <div class="chart-sub">Clima · hidrologia · sistema elétrico</div>
            <div class="chart-placeholder">Gráfico de séries temporais será alimentado pelo Databricks</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# TAB 5 — Modelo
# ------------------------------------------------------------

with tabs[4]:
    st.markdown(
        """
        <div class="section-head">
          <div class="section-title">
            <h2>Como transformamos sinais em previsão?</h2>
            <p>O objetivo é classificar o risco de bandeira vermelha em três horizontes.</p>
          </div>
        </div>

        <div class="question">
          <div class="question-bar"></div>
          <div style="width:100%;">
            <div class="eyebrow">Pipeline preditivo</div>
            <div class="question-text">
              Clima + Hidrologia + Sistema elétrico + Histórico
              → Feature Engineering → Modelo → Probabilidade M+1 / M+2 / M+3
            </div>
          </div>
        </div>

        <div class="cards" style="margin-top:18px;">
          <div class="risk-card" style="--card-color:#087cff;">
            <div class="risk-inner">
              <div class="risk-label">Horizonte</div>
              <div class="risk-value" style="font-size:24px;">M+1</div>
              <div class="risk-note">Target: bandeira vermelha no próximo mês</div>
            </div>
          </div>
          <div class="risk-card" style="--card-color:#087cff;">
            <div class="risk-inner">
              <div class="risk-label">Horizonte</div>
              <div class="risk-value" style="font-size:24px;">M+2</div>
              <div class="risk-note">Target: bandeira vermelha em dois meses</div>
            </div>
          </div>
          <div class="risk-card" style="--card-color:#087cff;">
            <div class="risk-inner">
              <div class="risk-label">Horizonte</div>
              <div class="risk-value" style="font-size:24px;">M+3</div>
              <div class="risk-note">Target: bandeira vermelha em três meses</div>
            </div>
          </div>
          <div class="risk-card" style="--card-color:#00b86b;">
            <div class="risk-inner">
              <div class="risk-label">Saída</div>
              <div class="risk-value" style="font-size:24px;">%</div>
              <div class="risk-note">Probabilidade estimada</div>
            </div>
          </div>
        </div>

        <div class="section-head">
          <div class="section-title">
            <h2>Avaliação</h2>
            <p>Métricas e matriz de confusão serão preenchidas com os resultados reais.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "Métricas do modelo ainda não são exibidas nesta etapa visual para evitar números fictícios."
    )


# ------------------------------------------------------------
# TAB 6 — Metodologia
# ------------------------------------------------------------

with tabs[5]:
    st.markdown(
        """
        <div class="section-head">
          <div class="section-title">
            <h2>Da informação à decisão</h2>
            <p>Arquitetura e narrativa do projeto.</p>
          </div>
        </div>

        <div class="question">
          <div class="question-bar"></div>
          <div style="width:100%;">
            <div class="eyebrow">Arquitetura de dados</div>
            <div class="question-text">
              Fontes → Raw → Trusted → Refined → Feature Engineering →
              Modelo Preditivo → Probabilidade M+1 / M+2 / M+3 → Streamlit
            </div>
          </div>
        </div>

        <div class="impact" style="margin-top:18px;">
          <div class="impact-intro">
            <div class="eyebrow">Princípio</div>
            <h3>O objetivo não é prever uma certeza.</h3>
            <p>
              É transformar dados disponíveis hoje em um sinal antecipado
              de risco para apoiar decisões sobre os próximos meses.
            </p>
          </div>
          <div class="impact-grid">
            <div class="impact-card">
              <div class="impact-icon">01</div>
              <h4>FONTES</h4>
              <p>ANEEL, INMET e indicadores do sistema elétrico.</p>
            </div>
            <div class="impact-card">
              <div class="impact-icon">02</div>
              <h4>CAMADAS</h4>
              <p>Organização e tratamento em Raw, Trusted e Refined.</p>
            </div>
            <div class="impact-card">
              <div class="impact-icon">03</div>
              <h4>PRODUTO</h4>
              <p>Probabilidade de bandeira vermelha em três horizontes.</p>
            </div>
          </div>
        </div>

        <div class="section-head">
          <div class="section-title">
            <h2>Transparência</h2>
            <p>As probabilidades apresentadas deverão vir do modelo treinado e validado.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(closing_section(), unsafe_allow_html=True)
