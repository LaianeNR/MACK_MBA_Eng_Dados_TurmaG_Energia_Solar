import streamlit as st
import pandas as pd

st.set_page_config(page_title="Previsão de Bandeiras", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.stApp {background: radial-gradient(circle at 4% 0%, rgba(255,193,7,.11), transparent 24%), radial-gradient(circle at 96% 4%, rgba(0,119,255,.09), transparent 28%), repeating-linear-gradient(90deg, rgba(16,42,67,.018) 0px, rgba(16,42,67,.018) 1px, transparent 1px, transparent 80px), linear-gradient(180deg, #f7f9fc 0%, #eef3f8 100%);}
.block-container {max-width:1450px; padding-top:2rem; padding-bottom:4rem;}
.hero {padding:10px 0 28px; border-bottom:1px solid #d8e2ec; margin-bottom:18px;}
.hero-topline,.section-number,.info-label,.risk-label {color:#1677ff; font-size:10px; font-weight:800; letter-spacing:1.8px; text-transform:uppercase;}
.hero-title {font-size:40px; font-weight:850; letter-spacing:-2px; color:#102a43; line-height:1.05;}
.hero-subtitle,.section-description,.info-text,.risk-caption {color:#627d98;}
.hero-subtitle {font-size:14px; margin-top:8px;}
.section {margin-top:34px; margin-bottom:18px; padding-left:15px; border-left:4px solid #f4b942;}
.section-title {font-size:23px; font-weight:850; color:#102a43; letter-spacing:-.5px;}
.section-description {font-size:13px; margin-top:5px;}
.banner {background:radial-gradient(circle at 92% 15%, rgba(255,209,102,.20), transparent 24%), radial-gradient(circle at 70% 100%, rgba(22,119,255,.13), transparent 35%), linear-gradient(135deg,#071d35,#0b3559); border-radius:20px; padding:28px 32px; margin:24px 0; box-shadow:0 14px 40px rgba(7,29,53,.14);}
.banner-label {color:#8ec5ff; font-size:10px; font-weight:800; letter-spacing:1.5px; text-transform:uppercase;}
.banner-title {color:#ffd166; font-size:21px; font-weight:850; margin-top:7px;}
.banner-text {color:#d9e8f5; font-size:13px; line-height:1.7; max-width:950px; margin-top:9px;}
.kpi,.risk-card,.info-box {background:rgba(255,255,255,.96); border:1px solid #d9e2ec; border-radius:17px; box-shadow:0 8px 25px rgba(16,42,67,.055);}
.kpi {padding:20px; min-height:125px;}
.kpi-label {color:#627d98; font-size:10px; font-weight:850; letter-spacing:1px; margin-bottom:10px;}
.kpi-value {color:#102a43; font-size:27px; font-weight:850; letter-spacing:-1px;}
.kpi-caption {color:#829ab1; font-size:11px; margin-top:7px;}
.risk-card {padding:20px; min-height:145px; text-align:center;}
.risk-label {color:#627d98;}
.risk-value {color:#102a43; font-size:34px; font-weight:850; margin-top:12px;}
.risk-caption {color:#829ab1; font-size:11px; margin-top:6px;}
.info-box {padding:23px; min-height:170px;}
.info-title {color:#102a43; font-size:18px; font-weight:800; margin-bottom:10px;}
.info-text {font-size:12px; line-height:1.7;}
.stTabs [data-baseweb="tab-list"] {gap:28px; border-bottom:1px solid #d9e2ec;}
.stTabs [data-baseweb="tab"] {font-weight:750; color:#627d98;}
.stTabs [aria-selected="true"] {color:#102a43 !important;}
div[data-testid="stDataFrame"] {border:1px solid #d9e2ec; border-radius:14px; overflow:hidden;}
.footer {text-align:center; color:#829ab1; font-size:10px; padding-top:50px; letter-spacing:.3px;}
</style>
""", unsafe_allow_html=True)

# FONTE TEMPORÁRIA: usada apenas para testar o novo layout.
# Na etapa seguinte será substituída por consultas ao Databricks.
ARQUIVOS = {"ENA":"./trusted/ena_mensal.parquet", "Bandeiras":"./trusted/bandeira_mensal.parquet"}

@st.cache_data
def carregar_base(caminho):
    try: return pd.read_parquet(caminho)
    except Exception: return None

def preparar_data(df):
    if df is None: return None
    df=df.copy()
    if "mes" in df.columns:
        df["mes"]=pd.to_datetime(df["mes"].astype(str), errors="coerce")
        df=df.dropna(subset=["mes"]).sort_values("mes").reset_index(drop=True)
    return df

def secao(n,t,d):
    st.markdown(f'<div class="section"><div class="section-number">{n}</div><div class="section-title">{t}</div><div class="section-description">{d}</div></div>', unsafe_allow_html=True)

def banner(l,t,x):
    st.markdown(f'<div class="banner"><div class="banner-label">{l}</div><div class="banner-title">{t}</div><div class="banner-text">{x}</div></div>', unsafe_allow_html=True)

def kpi(col,t,v,c):
    with col: st.markdown(f'<div class="kpi"><div class="kpi-label">{t}</div><div class="kpi-value">{v}</div><div class="kpi-caption">{c}</div></div>', unsafe_allow_html=True)

def risco(col,h):
    with col: st.markdown(f'<div class="risk-card"><div class="risk-label">RISCO {h}</div><div class="risk-value">—</div><div class="risk-caption">Saída do modelo pendente</div></div>', unsafe_allow_html=True)

df_ena=preparar_data(carregar_base(ARQUIVOS["ENA"]))
df_bandeiras=preparar_data(carregar_base(ARQUIVOS["Bandeiras"]))

st.markdown('<div class="hero"><div class="hero-topline">DATA INTELLIGENCE • ELECTRICITY</div><div class="hero-title">⚡ PREVISÃO DE BANDEIRAS</div><div class="hero-subtitle">Inteligência de dados aplicada à antecipação do risco tarifário no setor elétrico brasileiro</div></div>', unsafe_allow_html=True)

tab_visao,tab_prev,tab_vars,tab_hist,tab_modelo,tab_met=st.tabs(["🔎 Visão Geral","🤖 Previsão","🌧️ Variáveis","📈 Histórico","🧠 Modelo","📚 Metodologia"])

with tab_visao:
    banner("01 / VISÃO EXECUTIVA","⚡ ANTECIPAÇÃO DO RISCO TARIFÁRIO","O dashboard apresenta a evolução histórica das bandeiras e prepara a visualização das probabilidades de ocorrência de bandeira vermelha nos horizontes M+1, M+2 e M+3.")
    secao("01","Indicadores principais","Resumo do estado atual e dos horizontes de previsão.")
    c1,c2,c3,c4=st.columns(4)
    kpi(c1,"BANDEIRA ATUAL","—","consulta Databricks na versão final")
    risco(c2,"M+1"); risco(c3,"M+2"); risco(c4,"M+3")
    secao("02","O problema em foco","O objetivo é estimar o risco de ocorrência de bandeira vermelha a partir de variáveis disponíveis até o momento da previsão.")
    a,b=st.columns(2)
    with a:
        st.markdown('<div class="info-box"><div class="info-label">TARGET</div><div class="info-title">Bandeira vermelha</div><div class="info-text">A previsão é tratada como uma classificação binária: <b>1 = bandeira vermelha</b> e <b>0 = demais situações</b>.<br><br>O modelo gera uma probabilidade para cada horizonte de previsão.</div></div>',unsafe_allow_html=True)
    with b:
        st.markdown('<div class="info-box"><div class="info-label">HORIZONTES</div><div class="info-title">M+1 • M+2 • M+3</div><div class="info-text">A análise considera três horizontes temporais: próximo mês, dois meses à frente e três meses à frente.<br><br>O objetivo é apoiar a antecipação do risco tarifário.</div></div>',unsafe_allow_html=True)

with tab_prev:
    banner("02 / MODELO PREDITIVO","🤖 PROBABILIDADE DE BANDEIRA VERMELHA","Os valores abaixo serão alimentados pela saída do modelo preditivo quando a integração com o Databricks estiver concluída.")
    secao("01","Horizontes de previsão","Probabilidade estimada de ocorrência de bandeira vermelha.")
    c1,c2,c3=st.columns(3); risco(c1,"M+1"); risco(c2,"M+2"); risco(c3,"M+3")
    st.info("Aguardando a saída do modelo. Nenhum percentual é inventado nesta etapa.")
    secao("02","Como interpretar","A probabilidade representa a estimativa do modelo para a classe vermelha.")
    st.markdown("Se o modelo apresentar 70% para M+1, isso significa que, segundo o modelo e as variáveis fornecidas, a probabilidade estimada de ocorrência de bandeira vermelha no próximo mês é de 70%. A probabilidade não deve ser interpretada como certeza ou causalidade.")

with tab_vars:
    banner("03 / VARIÁVEIS EXPLICATIVAS","🌧️ O QUE ESTÁ ASSOCIADO AO RISCO TARIFÁRIO?","Visualização dos indicadores climáticos, hidrológicos e energéticos utilizados ou avaliados para a modelagem.")
    secao("01","Indicadores disponíveis","Exploração dos indicadores presentes na base histórica disponível.")
    if df_ena is not None and not df_ena.empty:
        cols=[c for c in df_ena.columns if c!="mes" and pd.api.types.is_numeric_dtype(df_ena[c])]
        if cols:
            sel=st.multiselect("Selecione os indicadores",cols,default=cols[:min(3,len(cols))],key="vars")
            if sel: st.line_chart(df_ena[["mes"]+sel].set_index("mes"),use_container_width=True)
        else: st.info("A base atual não possui indicadores numéricos disponíveis.")
    else: st.warning("Base ENA não disponível nesta versão temporária.")
    secao("02","Variáveis do modelo","Indicadores previstos para a análise final no Databricks.")
    st.markdown("**Clima:** precipitação média, precipitação acumulada, % da normal, temperatura e umidade.\n\n**Hidrologia:** EAR e ENA.\n\n**Sistema elétrico:** CMO e carga.\n\n**Histórico:** bandeira anterior.")

with tab_hist:
    banner("04 / SÉRIE HISTÓRICA","📈 COMPORTAMENTO DAS BANDEIRAS","A série histórica permite observar o comportamento das bandeiras e dos indicadores utilizados na análise.")
    if df_bandeiras is None or df_bandeiras.empty: st.warning("Base histórica de bandeiras não disponível.")
    else:
        secao("01","Histórico das bandeiras","Evolução temporal dos registros disponíveis.")
        candidatos=[c for c in ["NivelBandeira","nivel_bandeira","VlrAdicionalBandeira","ValorAdicionalBandeira"] if c in df_bandeiras.columns]
        if candidatos:
            v=candidatos[0]; dados=df_bandeiras[["mes",v]].copy(); dados[v]=pd.to_numeric(dados[v],errors="coerce"); st.line_chart(dados.dropna().set_index("mes")[v],use_container_width=True)
        st.dataframe(df_bandeiras.tail(12),use_container_width=True,hide_index=True)

with tab_modelo:
    banner("05 / AVALIAÇÃO PREDITIVA","🧠 DESEMPENHO DOS MODELOS","Área reservada para apresentar os resultados do treinamento, backtest e avaliação dos modelos para M+1, M+2 e M+3.")
    secao("01","Horizontes avaliados","Cada horizonte possui um alvo específico de previsão.")
    st.dataframe(pd.DataFrame({"Horizonte":["M+1","M+2","M+3"],"Alvo":["Bandeira vermelha no mês seguinte","Bandeira vermelha em dois meses","Bandeira vermelha em três meses"],"Status":["Aguardando modelo"]*3}),use_container_width=True,hide_index=True)
    secao("02","Métricas","Os valores reais serão preenchidos após a validação dos modelos.")
    c1,c2,c3,c4=st.columns(4); kpi(c1,"ACURÁCIA","—","resultado do backtest"); kpi(c2,"PRECISÃO","—","classe vermelha"); kpi(c3,"RECALL","—","classe vermelha"); kpi(c4,"F1 / ROC-AUC","—","avaliação do modelo")

with tab_met:
    banner("06 / ARQUITETURA DE DADOS","📚 DADOS → MODELO → PREVISÃO","O dashboard representa a camada de visualização da solução de dados e previsão.")
    secao("01","Fluxo da solução","Arquitetura conceitual do projeto.")
    st.code("""Fontes de dados\n        ↓\nCamada Raw\n        ↓\nCamada Trusted\n        ↓\nCamada Refined\n        ↓\nFeature Engineering\n        ↓\nModelo Preditivo\n        ↓\nProbabilidade M+1 / M+2 / M+3\n        ↓\nDashboard Streamlit""",language="text")
    secao("02","Camada visual","Na versão final, o Streamlit consultará os dados disponibilizados no Databricks.")
    st.markdown("**Arquitetura planejada:** `Databricks → SQL Warehouse → Streamlit`\n\nO dashboard não substitui as camadas de dados. Ele apresenta indicadores, histórico e resultados produzidos a partir delas.")
    secao("03","Escopo da previsão","Objetivo da aplicação.")
    st.markdown("O foco da aplicação é antecipar o risco de ocorrência de **bandeira tarifária vermelha** nos horizontes **M+1, M+2 e M+3**, utilizando variáveis climáticas, hidrológicas e energéticas disponíveis no projeto.")

st.markdown('<div class="footer">PREVISÃO DE BANDEIRAS • MBA EM ENGENHARIA DE DADOS • Projeto de análise preditiva do setor elétrico brasileiro</div>',unsafe_allow_html=True)
