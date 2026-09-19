import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(
    page_title="Crash Copilot Pro",
    page_icon="🍏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# STYLES CSS : APPLE PRO, GLASSMORPHISM & NEUMORPHISM
# ==========================================
st.markdown("""
    <style>
    /* 1. Garder le menu mobile et supprimer définitivement les logos */
    
    /* Rendre l'en-tête transparent pour conserver le bouton menu (☰) sur téléphone */
    header { background: transparent !important; box-shadow: none !important; }
    
    /* Cacher les boutons de base en haut à droite (GitHub, Déployer, etc.) */
    [data-testid="stToolbar"] { visibility: hidden !important; display: none !important; }
    #MainMenu { visibility: hidden !important; display: none !important; }
    footer { visibility: hidden !important; display: none !important; }
    
    /* Détruire les logos persistants en bas à droite */
    .stDeployButton { visibility: hidden !important; display: none !important; }
    [data-testid="stAppDeployButton"] { visibility: hidden !important; display: none !important; }
    div[class^='viewerBadge'] { visibility: hidden !important; display: none !important; }
    [data-testid="stStatusWidget"] { visibility: hidden !important; display: none !important; }
    
    .stApp {
        background-color: #000000;
        background-image: radial-gradient(circle at 15% 50%, rgba(20, 30, 48, 0.8), transparent 50%),
                          radial-gradient(circle at 85% 30%, rgba(10, 15, 30, 0.8), transparent 50%);
        color: #f5f5f7;
    }

    /* 2. Customisation de la barre latérale (iOS Frosted Glass) */
    section[data-testid="stSidebar"] {
        background: rgba(28, 28, 30, 0.4) !important;
        backdrop-filter: blur(50px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(50px) saturate(200%) !important;
        border-right: 0.5px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* 3. Boîtes de Signalisation (Style Dynamic Island / Notifications iOS) */
    .signal-box-green {
        background: rgba(48, 209, 88, 0.15);
        backdrop-filter: blur(40px) saturate(150%);
        -webkit-backdrop-filter: blur(40px) saturate(150%);
        border: 0.5px solid rgba(48, 209, 88, 0.4);
        border-radius: 24px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.2);
        color: #30d158;
        font-size: 20px;
        font-weight: 600;
        letter-spacing: -0.5px;
    }

    .signal-box-yellow {
        background: rgba(255, 159, 10, 0.15);
        backdrop-filter: blur(40px) saturate(150%);
        -webkit-backdrop-filter: blur(40px) saturate(150%);
        border: 0.5px solid rgba(255, 159, 10, 0.4);
        border-radius: 24px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.2);
        color: #ff9f0a;
        font-size: 20px;
        font-weight: 600;
        letter-spacing: -0.5px;
    }

    .signal-box-red {
        background: rgba(255, 69, 58, 0.15);
        backdrop-filter: blur(40px) saturate(150%);
        -webkit-backdrop-filter: blur(40px) saturate(150%);
        border: 0.5px solid rgba(255, 69, 58, 0.4);
        border-radius: 24px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.2);
        color: #ff453a;
        font-size: 20px;
        font-weight: 600;
        letter-spacing: -0.5px;
    }

    /* 4. Cartes KPI (Style Widgets iOS) */
    .kpi-card {
        background: rgba(44, 44, 46, 0.5);
        backdrop-filter: blur(40px) saturate(150%);
        -webkit-backdrop-filter: blur(40px) saturate(150%);
        border: 0.5px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s cubic-bezier(0.25, 1, 0.5, 1);
    }
    .kpi-card:hover {
        transform: scale(1.02);
        background: rgba(58, 58, 60, 0.6);
    }

    /* 5. Inputs (Neumorphism Tactile Enfoncé) */
    div[data-baseweb="input"] {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 0.5px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        box-shadow: inset 2px 4px 8px rgba(0, 0, 0, 0.6), 
                    inset -1px -1px 2px rgba(255, 255, 255, 0.03) !important;
    }
    div[data-baseweb="input"] input {
        color: #f5f5f7 !important;
        font-weight: 500 !important;
    }

    /* 6. Boutons (Style Apple Control Center) */
    .stButton>button, div[data-testid="stForm"] button {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(20px) saturate(150%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(150%) !important;
        border: 0.5px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px !important;
        color: #f5f5f7 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        padding: 12px 24px !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3),
                    inset 0 1px 1px rgba(255, 255, 255, 0.3) !important;
        transition: all 0.2s cubic-bezier(0.25, 1, 0.5, 1) !important;
    }

    .stButton>button:hover, div[data-testid="stForm"] button:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        transform: translateY(-2px) !important;
    }

    .stButton>button:active, div[data-testid="stForm"] button:active {
        transform: scale(0.97) !important;
        background: rgba(255, 255, 255, 0.05) !important;
        box-shadow: inset 1px 3px 6px rgba(0, 0, 0, 0.5) !important;
    }

    /* 7. Conteneur du Formulaire (Verre Dépoli) */
    div[data-testid="stForm"] {
        background: rgba(28, 28, 30, 0.4) !important;
        backdrop-filter: blur(40px) saturate(150%) !important;
        -webkit-backdrop-filter: blur(40px) saturate(150%) !important;
        border: 0.5px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 28px !important;
        padding: 30px !important;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4),
                    inset 0 1px 1px rgba(255, 255, 255, 0.1) !important;
    }

    /* Textes spécifiques */
    .apple-title { font-size: 34px; font-weight: 700; letter-spacing: -1px; margin-bottom: 5px; color: #f5f5f7;}
    .apple-subtitle { font-size: 17px; font-weight: 400; color: #86868b; margin-bottom: 30px;}
    .big-font { font-size: 28px !important; font-weight: 700; letter-spacing: -0.5px; }
    .kpi-label { color: #86868b; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# INITIALISATION DE L'ÉTAT (SESSION STATE)
# ==========================================
if 'history' not in st.session_state:
    st.session_state.history = []
if 'capital' not in st.session_state:
    st.session_state.capital = 1100.0
if 'trades' not in st.session_state:
    st.session_state.trades = []
if 'current_target' not in st.session_state:
    st.session_state.current_target = 2.00

# ==========================================
# MOTEUR ALGORITHMIQUE (V12 : DOUBLE CHECK)
# ==========================================
def analyze_market_2x_strict(history):
    n = len(history)
    if n < 3:
        return "Calibrage en cours. Saisissez au moins 3 tours.", 2.00, "yellow"

    last_cote = history[-1]

    if n >= 4:
        if all(x < 1.20 for x in history[-4:]):
            return "Alerte : Chute anormale détectée. Ne jouez pas.", 2.00, "red"

    if last_cote >= 10.0:
        return "Correction anticipée suite à un pic. Patientez.", 2.00, "yellow"

    tours_bas_consecutifs = 0
    for cote in reversed(history):
        if cote >= 2.00:
            break
        tours_bas_consecutifs += 1

    if tours_bas_consecutifs >= 3:
        derniere_cote = history[-1]
        avant_derniere = history[-2]
        
        if derniere_cote > avant_derniere:
            return f"Signal validé. Volatilité ascendante après {tours_bas_consecutifs} crashs. Entrez à 2.00x.", 2.00, "green"
        elif tours_bas_consecutifs >= 4:
            return f"Épuisement statistique de la série. Probabilité de hausse optimale. Entrez à 2.00x.", 2.00, "green"
        else:
            return f"Instabilité : chute persistante malgré {tours_bas_consecutifs} crashs bas. Laissez passer.", 2.00, "yellow"

    return "Marché neutre. Conservez votre capital.", 2.00, "yellow"

# ==========================================
# INTERFACE UTILISATEUR (SIDEBAR)
# ==========================================
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-weight:600; font-size:20px; color:#f5f5f7;'>Réglages</h2>", unsafe_allow_html=True)
    
    st.markdown("<div style='color:#86868b; font-size:13px; font-weight:500; margin-bottom:10px;'>GESTION DU CAPITAL</div>", unsafe_allow_html=True)
    nouveau_capital = st.number_input("Bankroll actuelle (XAF)", min_value=0.0, step=50.0, value=st.session_state.capital, label_visibility="collapsed")
    if st.button("Actualiser", use_container_width=True):
        st.session_state.capital = nouveau_capital
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='color:#86868b; font-size:13px; font-weight:500; margin-bottom:10px;'>SÉCURITÉ</div>", unsafe_allow_html=True)
    plafond_mise = st.slider("Mise maximum (%)", min_value=0.5, max_value=10.0, value=2.0, step=0.5)

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    if st.button("Réinitialiser le système", use_container_width=True):
        st.session_state.history = []
        st.session_state.trades = []
        st.session_state.capital = 1100.0
        st.session_state.current_target = 2.00
        st.rerun()

# ==========================================
# CORPS DE LA PAGE PRINCIPALE (DASHBOARD)
# ==========================================
st.markdown("<div class='apple-title'>Crash Copilot Pro</div>", unsafe_allow_html=True)
st.markdown("<div class='apple-subtitle'>Intelligence algorithmique et protection du capital.</div>", unsafe_allow_html=True)

# --- Analyse en Temps Réel ---
signal_msg, target, css_class = analyze_market_2x_strict(st.session_state.history)
st.session_state.current_target = target

# --- Formulaire de Saisie ---
with st.form("entry_form", clear_on_submit=True):
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        st.markdown("<span style='color:#f5f5f7; font-weight:500;'>Résultat du crash (Côte)</span>", unsafe_allow_html=True)
        new_cote = st.number_input("", min_value=1.00, step=0.01, format="%.2f", label_visibility="collapsed")
    with col_in2:
        mise_conseillee = round(st.session_state.capital * (plafond_mise / 100.0), -1)
        st.markdown("<span style='color:#f5f5f7; font-weight:500;'>Mise investie (0 = Ignoré)</span>", unsafe_allow_html=True)
        mise_jouee = st.number_input("", min_value=0.0, step=10.0, value=max(50.0, mise_conseillee), label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("Analyser le tour", use_container_width=True)

if submitted:
    profit = 0.0
    res_final = "Pas joué"
    
    if mise_jouee > 0:
        if new_cote >= st.session_state.current_target:
            res_final = "Gagné"
            profit = (mise_jouee * st.session_state.current_target) - mise_jouee
        else:
            res_final = "Perdu"
            profit = -mise_jouee
        st.session_state.capital += profit
    else:
        res_final = "Pas joué"

    st.session_state.history.append(new_cote)
    
    trade_data = {
        "Tour": len(st.session_state.history),
        "Cote": new_cote,
        "Investissement": mise_jouee,
        "Bénéfice": profit,
        "Bankroll": st.session_state.capital
    }
    st.session_state.trades.append(trade_data)
    st.rerun()

st.write("")
st.write("")

# --- Affichage du Signal ---
st.markdown(f'<div class="signal-box-{css_class}">{signal_msg}<br><span style="font-size: 14px; font-weight: 500; opacity: 0.7; letter-spacing: 0;">Mise suggérée : {round(st.session_state.capital * (plafond_mise / 100.0), -1):.0f} XAF</span></div>', unsafe_allow_html=True)

st.write("")
st.write("")

# ==========================================
# STATISTIQUES & PERFORMANCES (WIDGETS)
# ==========================================
nb_tours = len(st.session_state.history)
max_cote = max(st.session_state.history) if nb_tours > 0 else 0.0
trades_joues = [t for t in st.session_state.trades if t['Investissement'] > 0 and t['Bénéfice'] != 0.0]
win_rate = (sum(1 for t in trades_joues if t['Bénéfice'] > 0) / len(trades_joues) * 100) if trades_joues else 0.0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Capital Actuel</div><br><div class='big-font' style='color:{'#30d158' if st.session_state.capital >= 1100 else '#ff453a'};'>{st.session_state.capital:.0f} XAF</div></div>", unsafe_allow_html=True)
with kpi2:
    st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Précision (2.00x)</div><br><div class='big-font' style='color:#f5f5f7;'>{win_rate:.0f}%</div></div>", unsafe_allow_html=True)
with kpi3:
    st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Pic Maximum</div><br><div class='big-font' style='color:#0a84ff;'>{max_cote:.2f}x</div></div>", unsafe_allow_html=True)
with kpi4:
    st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Tours Analysés</div><br><div class='big-font' style='color:#f5f5f7;'>{nb_tours}</div></div>", unsafe_allow_html=True)

st.write("")
st.write("")

# ==========================================
# GRAPHIQUES (STYLE APPLE BOURSE / SANTÉ)
# ==========================================
gcol1, gcol2 = st.columns(2)

with gcol1:
    st.markdown("<h3 style='font-size:18px; font-weight:600; color:#f5f5f7; margin-bottom:15px;'>Évolution du Capital</h3>", unsafe_allow_html=True)
    if len(st.session_state.trades) > 0:
        df_trades = pd.DataFrame(st.session_state.trades)
        fig_bank = go.Figure()
        fig_bank.add_trace(go.Scatter(
            x=list(range(len(df_trades))), 
            y=df_trades['Bankroll'],
            mode='lines',
            line=dict(color='#0a84ff', width=3, shape='spline'),
            fill='tozeroy',
            fillcolor='rgba(10, 132, 255, 0.15)'
        ))
        fig_bank.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            height=250, margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=False, visible=False), 
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', gridwidth=1, tickfont=dict(color='#86868b'))
        )
        st.plotly_chart(fig_bank, use_container_width=True, config={'displayModeBar': False})
    else:
        st.markdown("<div class='kpi-card' style='height:250px; display:flex; align-items:center; justify-content:center; color:#86868b;'>En attente de données...</div>", unsafe_allow_html=True)

with gcol2:
    st.markdown("<h3 style='font-size:18px; font-weight:600; color:#f5f5f7; margin-bottom:15px;'>Tendances des Côtes</h3>", unsafe_allow_html=True)
    if nb_tours > 0:
        colors = ['#30d158' if c >= 2.0 else '#ff453a' for c in st.session_state.history]
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=list(range(1, nb_tours + 1)),
            y=st.session_state.history,
            marker_color=colors,
            marker_line_width=0,
            opacity=0.8
        ))
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            height=250, margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=False, visible=False), 
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', gridwidth=1, tickfont=dict(color='#86868b'))
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
    else:
        st.markdown("<div class='kpi-card' style='height:250px; display:flex; align-items:center; justify-content:center; color:#86868b;'>En attente de données...</div>", unsafe_allow_html=True)
