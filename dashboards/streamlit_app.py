import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Previsão de Bandeiras | Energy Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# IDENTIDADE VISUAL
# Navy = identidade | Azul = tecnologia | Verde/Amarelo/Vermelho = risco
# =========================================================
st.markdown("""
<style>
.stApp {
    background:#F3F6FA;
    color: #071A33;
}
.block-container { max-width: 1480px; padding-top: 1.25rem; padding-bottom: 4rem; }

/* HERO */
.hero {
    position: relative; overflow: hidden; padding: 30px 34px 31px;
    border-radius: 25px; margin-bottom: 18px;
    background:#061A2F;
    box-shadow: 0 20px 48px rgba(7,26,51,.17);
    border:2px solid #0066FF;
}
.hero:after { content:"⚡"; position:absolute; right:36px; bottom:-28px; font-size:135px; color:#0A3156; transform:rotate(8deg); }
.hero-topline,.section-number,.info-label,.risk-label { color:#0066FF; font-size:10px; font-weight:900; letter-spacing:1.9px; text-transform:uppercase; }
.hero-title { color:#fff; font-size:43px; font-weight:950; letter-spacing:-2.2px; line-height:1.02; margin-top:7px; position:relative; z-index:1; }
.hero-title span { color:#00C2FF; }
.hero-subtitle { color:#E7F2FA; font-size:14px; margin-top:11px; max-width:980px; line-height:1.55; position:relative; z-index:1; }
.hero-badge { display:inline-block; margin-top:18px; padding:7px 12px; border-radius:999px; background:#0B3156; border:1px solid #1D527E; color:#E9F8FF; font-size:10px; font-weight:850; letter-spacing:1px; position:relative; z-index:1; }

/* TABS */
.stTabs [data-baseweb="tab-list"] { gap:5px; padding:5px; background:#FFFFFF; border:2px solid #D6E3EE; border-radius:15px; box-shadow:0 7px 22px rgba(7,26,51,.055); }
.stTabs [data-baseweb="tab"] { color:#63758A; font-weight:850; border-radius:10px; padding:9px 13px; }
.stTabs [aria-selected="true"] { color:#FFFFFF !important; background:#0066FF; }

/* SECTIONS */
.section { margin-top:31px; margin-bottom:16px; padding:2px 0 2px 15px; border-left:5px solid #0066FF; }
.section-title { color:#071A33; font-size:23px; font-weight:920; letter-spacing:-.6px; }
.section-description { color:#607089; font-size:13px; margin-top:5px; line-height:1.5; }

/* BANNERS */
.banner { position:relative; overflow:hidden; background:#071A33; border-radius:20px; padding:27px 31px; margin:23px 0; box-shadow:0 14px 38px rgba(7,26,51,.15); }
.banner:after { content:"⚡"; position:absolute; right:35px; top:7px; font-size:88px; color:#0B3156; transform:rotate(10deg); }
.banner-label { color:#00C2FF; font-size:10px; font-weight:900; letter-spacing:1.7px; text-transform:uppercase; }
.banner-title { color:#fff; font-size:22px; font-weight:920; margin-top:7px; }
.banner-text { color:#E7F2FA; font-size:13px; line-height:1.7; max-width:1080px; margin-top:9px; }

/* CARDS */
.kpi,.risk-card,.info-box,.story-card { background:#FFFFFF; border:1px solid #CFDCE8; border-radius:18px; box-shadow:0 9px 28px rgba(7,26,51,.065); }
.kpi { padding:20px; min-height:126px; border-top:5px solid #0066FF; }
.kpi-label { color:#607089; font-size:10px; font-weight:900; letter-spacing:1.1px; margin-bottom:10px; }
.kpi-value { color:#061A2F; font-size:31px; font-weight:920; letter-spacing:-1px; }
.kpi-caption { color:#8294A8; font-size:11px; margin-top:7px; }
.risk-card { padding:19px; min-height:153px; text-align:center; border-top:5px solid #0066FF; }
.risk-label { color:#607089; }
.risk-value { color:#061A2F; font-size:38px; font-weight:920; margin-top:12px; }
.risk-caption { color:#8294A8; font-size:11px; margin-top:6px; }
.info-box,.story-card { padding:23px; min-height:165px; }
.info-title { color:#071A33; font-size:18px; font-weight:900; margin-bottom:10px; }
.info-text { color:#607089; font-size:12px; line-height:1.75; }

/* STORY / FLOW */
.story-card { min-height:145px; border-top:4px solid #0066FF; }
.story-step { color:#0066FF; font-size:10px; font-weight:900; letter-spacing:1.3px; text-transform:uppercase; }
.story-title { color:#071A33; font-size:17px; font-weight:900; margin-top:7px; }
.story-text { color:#607089; font-size:12px; line-height:1.65; margin-top:7px; }
.flow { background:#FFFFFF; border:2px solid #CFDCE8; border-radius:20px; padding:22px; box-shadow:0 9px 28px rgba(7,26,51,.055); }
.flow-node { background:#FFFFFF; border:2px solid #D4E6F4; border-radius:13px; padding:13px 10px; text-align:center; font-weight:850; color:#173653; font-size:12px; }
.flow-arrow { text-align:center; color:#0066FF; font-size:18px; padding:4px 0; font-weight:900; }

.status-strip { padding:13px 16px; border-radius:13px; background:#E8F2FF; border:1px solid #A9CBFF; color:#31536F; font-size:12px; margin:15px 0; }
.question { background:#0066FF; color:white; border-radius:17px; padding:21px 24px; box-shadow:0 10px 27px rgba(7,26,51,.12); margin:15px 0; }
.question-label { color:#DDF7FF; font-size:10px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; }
.question-text { font-size:19px; font-weight:900; line-height:1.35; margin-top:6px; }
.footer { text-align:center; color:#66788C; font-size:10px; padding-top:50px; letter-spacing:.5px; }
a { color:#1479FF !important; }
div[data-testid="stDataFrame"] { border:1px solid #D5E3EE; border-radius:14px; overflow:hidden; }
.stAlert { border-radius:13px; }

.risk-green { border-top-color:#00B83D !important; }
.risk-yellow { border-top-color:#FFC400 !important; }
.risk-red { border-top-color:#E52521 !important; }
.risk-blue { border-top-color:#0066FF !important; }
.metric-blue { color:#0066FF !important; }
.metric-green { color:#00B83D !important; }
.metric-yellow { color:#B88600 !important; }
.metric-red { color:#E52521 !important; }
</style>
""", unsafe_allow_html=True)

# FONTE TEMPORÁRIA — somente para demonstração visual.
# Na integração final, estas leituras serão substituídas por consultas ao Databricks.
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
    st.markdown(f'<div class="section"><div class="section-number">{n}</div><div class="section-title">{titulo}</div><div class="section-description">{descricao}</div></div>', unsafe_allow_html=True)

def banner(label, titulo, texto):
    st.markdown(f'<div class="banner"><div class="banner-label">{label}</div><div class="banner-title">{titulo}</div><div class="banner-text">{texto}</div></div>', unsafe_allow_html=True)

def kpi(col, titulo, valor, legenda):
    with col:
        st.markdown(f'<div class="kpi"><div class="kpi-label">{titulo}</div><div class="kpi-value">{valor}</div><div class="kpi-caption">{legenda}</div></div>', unsafe_allow_html=True)

def risco(col, horizonte):
    with col:
        st.markdown(f'<div class="risk-card"><div class="risk-label">RISCO {horizonte}</div><div class="risk-value">—</div><div class="risk-caption">Saída do modelo pendente</div></div>', unsafe_allow_html=True)

def story_card(col, passo, titulo, texto):
    with col:
        st.markdown(f'<div class="story-card"><div class="story-step">{passo}</div><div class="story-title">{titulo}</div><div class="story-text">{texto}</div></div>', unsafe_allow_html=True)

df_ena = preparar_data(carregar_base(ARQUIVOS["ENA"]))
df_bandeiras = preparar_data(carregar_base(ARQUIVOS["Bandeiras"]))

st.markdown(
    '<div class="hero">'
    '<div class="hero-topline">ENERGY INTELLIGENCE • PREDICTIVE ANALYTICS</div>'
    '<div class="hero-title">⚡ PREVISÃO DE <span>BANDEIRAS</span></div>'
    '<div class="hero-subtitle">Inteligência de dados aplicada à antecipação do risco tarifário no setor elétrico brasileiro</div>'
    '<div class="hero-badge">M+1 • M+2 • M+3 &nbsp; | &nbsp; CLASSIFICAÇÃO DE RISCO &nbsp; | &nbsp; DATA &amp; ELECTRICITY</div>'
    '</div>', unsafe_allow_html=True,
)

tab_visao, tab_prev, tab_vars, tab_hist, tab_modelo, tab_met = st.tabs([
    "🔎 Visão Geral", "🤖 Previsão", "🌧️ Variáveis", "📈 Histórico", "🧠 Modelo", "📚 Metodologia"
])

with tab_visao:
    banner("01 / VISÃO EXECUTIVA", "⚡ ANTECIPAR O RISCO ANTES DA BANDEIRA", "A bandeira tarifária é observada no presente. O desafio do projeto é olhar para os sinais disponíveis hoje e estimar a probabilidade de bandeira vermelha nos próximos meses.")
    st.markdown('<div class="question"><div class="question-label">PERGUNTA DE NEGÓCIO</div><div class="question-text">Com as informações disponíveis hoje, conseguimos estimar o risco de bandeira vermelha em M+1, M+2 e M+3?</div></div>', unsafe_allow_html=True)

    secao("01", "Painel executivo", "A resposta final será apresentada em três horizontes futuros.")
    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "BANDEIRA ATUAL", "—", "consulta Databricks na versão final")
    risco(c2, "M+1")
    risco(c3, "M+2")
    risco(c4, "M+3")

    secao("02", "A história em uma linha", "Do dado bruto ao sinal de risco para tomada de decisão.")
    a,b,c,d = st.columns(4)
    story_card(a, "01 • CONTEXTO", "O sistema muda", "Clima, hidrologia, demanda e condições de operação variam ao longo do tempo.")
    story_card(b, "02 • SINAIS", "Os dados registram", "Construímos variáveis históricas, defasagens e indicadores para representar o contexto.")
    story_card(c, "03 • MODELO", "O modelo aprende", "A classificação usa o histórico para estimar a ocorrência de bandeira vermelha.")
    story_card(d, "04 • PREVISÃO", "O risco é antecipado", "O resultado esperado é uma probabilidade para M+1, M+2 e M+3.")

    secao("03", "O que estamos prevendo?", "Definição objetiva do alvo para a modelagem.")
    x,y = st.columns(2)
    with x:
        st.markdown('<div class="info-box"><div class="info-label">TARGET</div><div class="info-title">🚦 Bandeira vermelha</div><div class="info-text">Classificação binária: <b>1 = bandeira vermelha</b> e <b>0 = demais situações</b>. O resultado final será uma <b>probabilidade estimada</b>, não uma certeza.</div></div>', unsafe_allow_html=True)
    with y:
        st.markdown('<div class="info-box"><div class="info-label">HORIZONTES</div><div class="info-title">M+1 • M+2 • M+3</div><div class="info-text">Três alvos futuros permitem observar como o risco se comporta no curto prazo e conforme aumenta o horizonte de previsão.</div></div>', unsafe_allow_html=True)

with tab_prev:
    banner("02 / PREVISÃO", "🔮 QUAL É O RISCO À FRENTE?", "A interface foi desenhada para transformar a saída do modelo em uma leitura executiva: probabilidade de bandeira vermelha para cada horizonte futuro.")
    secao("01", "Três horizontes, uma leitura", "Quanto maior a probabilidade estimada, maior o sinal de atenção para aquele horizonte.")
    c1,c2,c3 = st.columns(3)
    risco(c1,"M+1"); risco(c2,"M+2"); risco(c3,"M+3")
    st.markdown('<div class="status-strip">🔵 <b>Status da versão:</b> os percentuais permanecem vazios até a integração com a saída real do modelo. Nenhuma probabilidade é inventada nesta etapa.</div>', unsafe_allow_html=True)
    secao("02", "Como ler a previsão", "Probabilidade é um sinal de risco, não uma promessa do que acontecerá.")
    st.markdown('<div class="info-box"><div class="info-label">EXEMPLO DE INTERPRETAÇÃO</div><div class="info-title">Se M+1 apresentar 70%</div><div class="info-text">Isso significa que, dadas as informações utilizadas pelo modelo, a <b>probabilidade estimada</b> de ocorrência de bandeira vermelha no mês seguinte é de 70%. O percentual não representa certeza e não permite concluir, sozinho, que uma variável causou a mudança de bandeira.</div></div>', unsafe_allow_html=True)

with tab_vars:
    banner("03 / SINAIS", "🌧️ O QUE PODE AJUDAR A ANTECIPAR O RISCO?", "O modelo reúne sinais de diferentes dimensões do sistema. A ideia é representar o contexto disponível antes do mês que será previsto.")
    secao("01", "Três famílias de sinais", "Clima, hidrologia e sistema elétrico complementam a leitura temporal do risco.")
    a,b,c = st.columns(3)
    story_card(a,"CLIMA","🌧️ Clima","Precipitação média, acumulada, percentual da normal, temperatura e umidade.")
    story_card(b,"HIDROLOGIA","💧 Hidrologia","EAR e ENA, incluindo histórico, defasagens e variações quando disponíveis.")
    story_card(c,"SISTEMA","⚡ Sistema elétrico","CMO, carga e histórico de bandeiras como sinais das condições observadas.")

    secao("02", "Exploração dos dados", "A visualização abaixo permanece como demonstração até a migração definitiva para o Databricks.")
    if df_ena is not None and not df_ena.empty:
        cols = [c for c in df_ena.columns if c != "mes" and pd.api.types.is_numeric_dtype(df_ena[c])]
        if cols:
            sel = st.multiselect("Selecione os indicadores", cols, default=cols[:min(3,len(cols))], key="vars")
            if sel:
                st.line_chart(df_ena[["mes"] + sel].set_index("mes"), use_container_width=True)
        else:
            st.info("A base atual não possui indicadores numéricos disponíveis.")
    else:
        st.warning("Base ENA não disponível nesta versão temporária.")

with tab_hist:
    banner("04 / EVIDÊNCIA", "📈 ANTES DE PREVER O FUTURO, OLHAMOS PARA O PASSADO", "A série histórica permite contextualizar mudanças de bandeira, identificar padrões temporais e observar como os indicadores se comportaram antes de cada período.")
    if df_bandeiras is None or df_bandeiras.empty:
        st.warning("Base histórica de bandeiras não disponível.")
    else:
        secao("01", "Evolução das bandeiras", "Comportamento temporal dos registros disponíveis.")
        candidatos = [c for c in ["NivelBandeira","nivel_bandeira","VlrAdicionalBandeira","ValorAdicionalBandeira"] if c in df_bandeiras.columns]
        if candidatos:
            v = candidatos[0]
            dados = df_bandeiras[["mes",v]].copy(); dados[v] = pd.to_numeric(dados[v], errors="coerce")
            st.line_chart(dados.dropna().set_index("mes")[v], use_container_width=True)
        st.dataframe(df_bandeiras.tail(12), use_container_width=True, hide_index=True)

with tab_modelo:
    banner("05 / MODELAGEM", "🧠 DOS SINAIS À PROBABILIDADE", "O modelo transforma variáveis históricas e temporais em uma estimativa de risco. A avaliação será feita respeitando a ordem cronológica dos dados.")
    secao("01", "Como o modelo enxerga o problema", "A estrutura conceitual conecta os sinais observados aos três alvos futuros.")
    st.markdown('<div class="flow"><div class="flow-node">🌧️ CLIMA</div><div class="flow-arrow">↓</div><div class="flow-node">💧 HIDROLOGIA</div><div class="flow-arrow">↓</div><div class="flow-node">⚡ SISTEMA + HISTÓRICO</div><div class="flow-arrow">↓</div><div class="flow-node">FEATURE ENGINEERING<br><small>Lags • variações • médias</small></div><div class="flow-arrow">↓</div><div class="flow-node">🤖 MODELO DE CLASSIFICAÇÃO</div><div class="flow-arrow">↓</div><div class="flow-node">🔮 PROBABILIDADE DE BANDEIRA VERMELHA<br>M+1 • M+2 • M+3</div></div>', unsafe_allow_html=True)

    secao("02", "Horizontes avaliados", "Cada horizonte possui um alvo específico de previsão.")
    st.dataframe(pd.DataFrame({"Horizonte":["M+1","M+2","M+3"],"Alvo":["Bandeira vermelha no mês seguinte","Bandeira vermelha em dois meses","Bandeira vermelha em três meses"],"Status":["Aguardando modelo"]*3}), use_container_width=True, hide_index=True)

    secao("03", "Como saberemos se funciona?", "A avaliação deve olhar além da acurácia, especialmente porque a classe vermelha é menos frequente.")
    c1,c2,c3,c4 = st.columns(4)
    kpi(c1,"PRECISÃO","—","classe vermelha")
    kpi(c2,"RECALL","—","classe vermelha")
    kpi(c3,"F1","—","equilíbrio entre precisão e recall")
    kpi(c4,"ROC-AUC","—","capacidade de discriminação")

with tab_met:
    banner("06 / METODOLOGIA", "📚 DA FONTE À DECISÃO", "A arquitetura organiza os dados em camadas e conduz o processamento até a experiência final de previsão.")
    secao("01", "A jornada do dado", "Cada camada tem uma função na construção do produto analítico.")
    st.markdown('<div class="flow"><div class="flow-node">01 • FONTES<br><small>ANEEL • INMET • dados do sistema</small></div><div class="flow-arrow">↓</div><div class="flow-node">02 • RAW<br><small>dados de origem</small></div><div class="flow-arrow">↓</div><div class="flow-node">03 • TRUSTED<br><small>limpeza • padronização • qualidade</small></div><div class="flow-arrow">↓</div><div class="flow-node">04 • REFINED<br><small>dados analíticos integrados</small></div><div class="flow-arrow">↓</div><div class="flow-node">05 • FEATURE ENGINEERING<br><small>lags • variações • indicadores</small></div><div class="flow-arrow">↓</div><div class="flow-node">06 • MODELO PREDITIVO<br><small>classificação M+1 • M+2 • M+3</small></div><div class="flow-arrow">↓</div><div class="flow-node">07 • PRODUTO<br><small>probabilidade de bandeira vermelha</small></div></div>', unsafe_allow_html=True)

    secao("02", "Arquitetura de consumo", "O dashboard é a camada de apresentação da solução.")
    st.markdown('<div class="info-box"><div class="info-label">INTEGRAÇÃO PLANEJADA</div><div class="info-title">Databricks → SQL Warehouse → Streamlit</div><div class="info-text">Na versão final, os indicadores e resultados apresentados pelo dashboard serão alimentados pelas camadas de dados e pelas saídas reais do modelo. A versão atual usa Parquet apenas para validar a interface.</div></div>', unsafe_allow_html=True)

    secao("03", "Objetivo do produto", "A entrega final precisa responder a uma pergunta simples.")
    st.markdown('<div class="question"><div class="question-label">RESULTADO ESPERADO</div><div class="question-text">Transformar dados disponíveis hoje em um sinal antecipado de risco para os próximos 1, 2 e 3 meses.</div></div>', unsafe_allow_html=True)

st.markdown('<div class="footer">ENERGY INTELLIGENCE • PREVISÃO DE BANDEIRAS • MBA EM ENGENHARIA DE DADOS</div>', unsafe_allow_html=True)
