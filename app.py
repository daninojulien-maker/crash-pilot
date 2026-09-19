import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(
    page_title="Crash Copilot Pro V12 - Filtre Anti-Série Noire",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé (Mode Sombre Pro)
st.markdown("""
    <style>
    .big-font { font-size: 24px !important; font-weight: bold; }
    .signal-box-green { background-color: #0f5132; color: #d1e7dd; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #198754; font-size: 20px; font-weight: bold;}
    .signal-box-yellow { background-color: #664d03; color: #fff3cd; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #ffc107; font-size: 20px; font-weight: bold;}
    .signal-box-red { background-color: #842029; color: #f8d7da; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #dc3545; font-size: 20px; font-weight: bold;}
    .kpi-card { background-color: #1e1e1e; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #333; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# INITIALISATION DE L'ÉTAT (SESSION STATE)
# ==========================================
if 'history' not in st.session_state:
    st.session_state.history = []
if 'capital' not in st.session_state:
    st.session_state.capital = 1100.0  # Ton dernier capital connu
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
        return "🟡 OBSERVATION : Saisissez au moins 3 tours pour calibrer le filtre.", 2.00, "yellow"

    last_cote = history[-1]

    # 1. Alerte Rouge : Purge algorithmique (trop de crashs nuls)
    if n >= 4:
        if all(x < 1.20 for x in history[-4:]):
            return "🔴 ALERTE SÉCURITÉ : Purge du jeu en cours. Chute anormale. NE JOUEZ PAS.", 2.00, "red"

    # 2. Alerte Pic : Risque de correction immédiate
    if last_cote >= 10.0:
        return "🟡 OBSERVATION : Gros pic détecté, la correction arrive. Attendez.", 2.00, "yellow"

    # Comptage des cotes consécutives < 2.00x
    tours_bas_consecutifs = 0
    for cote in reversed(history):
        if cote >= 2.00:
            break
        tours_bas_consecutifs += 1

    # 3. Application des filtres de correction (Profondeur + Momentum)
    if tours_bas_consecutifs >= 3:
        derniere_cote = history[-1]
        avant_derniere = history[-2]
        
        # MÉTHODE 2 : Le Filtre de Momentum (Double vérification)
        # On regarde si la volatilité remonte (la chute ralentit)
        if derniere_cote > avant_derniere:
            return f"🟢 SIGNAL CONFIRMÉ : {tours_bas_consecutifs} crashs bas + Volatilité en hausse ({avant_derniere} ↗ {derniere_cote}). ACHAT 2.00x !", 2.00, "green"
        
        # Si la série atteint 4 crashs bas ou plus, épuisement de la probabilité
        elif tours_bas_consecutifs >= 4:
            return f"🟢 SIGNAL EXTRÊME : {tours_bas_consecutifs} crashs < 2.00x. Épuisement mathématique de la série noire. JOUER !", 2.00, "green"
        
        # Le piège est détecté : on a 3 crashs bas, mais la cote continue de creuser vers le bas
        else:
            return f"🔵 PATIENCE (PIÈGE ÉVITÉ) : {tours_bas_consecutifs} crashs bas, mais la chute s'aggrave ({avant_derniere} ↘ {derniere_cote}). Laissez passer.", 2.00, "yellow"

    return "🔵 OBSERVATION : Marché instable ou neutre. Conservez votre mise.", 2.00, "yellow"

# ==========================================
# INTERFACE UTILISATEUR (SIDEBAR)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2015/2015061.png", width=60)
    st.title("Configuration")
    
    st.subheader("💰 Gestion du Capital")
    nouveau_capital = st.number_input("Définir / Mettre à jour Bankroll (XAF)", min_value=0.0, step=50.0, value=st.session_state.capital)
    if st.button("Mettre à jour Bankroll", use_container_width=True):
        st.session_state.capital = nouveau_capital
        st.rerun()

    st.markdown("---")
    st.subheader("🛡️ Paramètres de Jeu")
    plafond_mise = st.slider("Plafond de mise max (% Bankroll)", min_value=0.5, max_value=10.0, value=2.0, step=0.5)

    st.markdown("---")
    if st.button("🔄 Réinitialiser l'historique", type="secondary", use_container_width=True):
        st.session_state.history = []
        st.session_state.trades = []
        st.session_state.capital = 1100.0
        st.session_state.current_target = 2.00
        st.rerun()

# ==========================================
# CORPS DE LA PAGE PRINCIPALE (DASHBOARD)
# ==========================================
st.title("🚀 Crash Copilot Pro v12 (Double Filtre Anti-Série)")
st.markdown("Algorithme ultra-sélectif : Évite les pièges des séries de crashs baissiers en exigeant une confirmation de momentum (rebond validé).")
st.write("")

# --- Analyse en Temps Réel ---
signal_msg, target, css_class = analyze_market_2x_strict(st.session_state.history)
st.session_state.current_target = target

# --- Formulaire de Saisie du Dernier Tour ---
st.subheader("🎯 Saisie du dernier tour")
with st.form("entry_form", clear_on_submit=True):
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        new_cote = st.number_input("Cote finale du Crash (ex: 2.35):", min_value=1.00, step=0.01, format="%.2f")
    with col_in2:
        mise_conseillee = round(st.session_state.capital * (plafond_mise / 100.0), -1)
        mise_jouee = st.number_input("Mise jouée (0 = Pas joué) (XAF):", min_value=0.0, step=10.0, value=max(50.0, mise_conseillee))

    submitted = st.form_submit_button("📝 Enregistrer et Analyser", use_container_width=True)

if submitted:
    profit = 0.0
    res_final = "Pas joué"
    
    # Automatisation du pari par rapport au 2.00x
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
        "Cote_Crash": new_cote,
        "Mise_XAF": mise_jouee,
        "Objectif": st.session_state.current_target,
        "Resultat": res_final,
        "Profit_XAF": profit,
        "Bankroll_Post_Tour": st.session_state.capital,
        "Heure": datetime.now().strftime("%H:%M:%S")
    }
    st.session_state.trades.append(trade_data)
    st.rerun()

st.write("")

# --- Affichage du Signal ---
st.subheader("⚡ Analyse & Signal pour le prochain tour")
st.markdown(f'<div class="signal-box-{css_class}">{signal_msg}<br><span style="font-size: 16px; font-weight: normal;">Objectif de sortie Auto : <b>2.00x</b> | Mise conseillée : <b>{round(st.session_state.capital * (plafond_mise / 100.0), -1):.0f} XAF</b></span></div>', unsafe_allow_html=True)
st.write("")

# ==========================================
# STATISTIQUES & PERFORMANCES
# ==========================================
st.subheader("📊 Statistiques & Performances")

nb_tours = len(st.session_state.history)
max_cote = max(st.session_state.history) if nb_tours > 0 else 0.0
trades_joues = [t for t in st.session_state.trades if t['Mise_XAF'] > 0 and t['Resultat'] != "Pas joué"]
win_rate = (sum(1 for t in trades_joues if t['Resultat'] == "Gagné") / len(trades_joues) * 100) if trades_joues else 0.0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown(f"<div class='kpi-card'>💰 Bankroll Actuelle<br><b class='big-font' style='color:{'#198754' if st.session_state.capital >= 1100 else '#dc3545'};'>{st.session_state.capital:.1f} XAF</b></div>", unsafe_allow_html=True)
with kpi2:
    st.markdown(f"<div class='kpi-card'>🎯 Taux de réussite (2.00x)<br><b class='big-font'>{win_rate:.1f} %</b><br><small>{len(trades_joues)} paris joués</small></div>", unsafe_allow_html=True)
with kpi3:
    st.markdown(f"<div class='kpi-card'>🔥 Plus haute côte<br><b class='big-font'>{max_cote:.2f} x</b></div>", unsafe_allow_html=True)
with kpi4:
    st.markdown(f"<div class='kpi-card'>📈 Nombre de tours<br><b class='big-font'>{nb_tours}</b></div>", unsafe_allow_html=True)

st.write("")

# --- Graphiques ---
gcol1, gcol2 = st.columns(2)

with gcol1:
    st.markdown("##### Évolution de la Bankroll")
    if len(st.session_state.trades) > 0:
        df_trades = pd.DataFrame(st.session_state.trades)
        fig_bank = go.Figure()
        fig_bank.add_trace(go.Scatter(
            x=list(range(len(df_trades))), 
            y=df_trades['Bankroll_Post_Tour'],
            mode='lines+markers',
            line=dict(color='#198754', width=2)
        ))
        fig_bank.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'), margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(showgrid=True, gridcolor='#333'), yaxis=dict(showgrid=True, gridcolor='#333')
        )
        st.plotly_chart(fig_bank, use_container_width=True)
    else:
        st.info("Enregistrez des paris pour afficher l'évolution.")

with gcol2:
    st.markdown("##### Côtes des derniers tours")
    if nb_tours > 0:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=list(range(1, nb_tours + 1)),
            y=st.session_state.history,
            marker_color='#0dcaf0'
        ))
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'), margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(showgrid=True, gridcolor='#333'), yaxis=dict(showgrid=True, gridcolor='#333')
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Aucune côte enregistrée.")

st.write("---")

# ==========================================
# HISTORIQUE DÉTAILLÉ
# ==========================================
st.subheader("📝 Historique détaillé")
if nb_tours > 0:
    df_history = pd.DataFrame(st.session_state.trades)
    st.dataframe(df_history, use_container_width=True)
    
    csv_data = df_history.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Télécharger CSV (Excel)",
        data=csv_data,
        file_name=f"Crash_Copilot_V12_Strict_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime='text/csv'
    )
else:
    st.info("Le journal des tours est vide pour le moment.")