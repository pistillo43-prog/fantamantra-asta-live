
import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, timedelta

st.set_page_config(
    page_title="FantaMantra Asta Live",
    page_icon="⚽",
    layout="wide"
)

# =========================
# CSS V5 - FANTALAB STYLE
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background:
        radial-gradient(circle at top left, rgba(34,197,94,0.16), transparent 28%),
        radial-gradient(circle at top right, rgba(59,130,246,0.16), transparent 28%),
        linear-gradient(135deg, #020617 0%, #0f172a 45%, #111827 100%);
    color: #f8fafc;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
    border-right: 1px solid rgba(148,163,184,0.18);
}

h1, h2, h3 {
    color: #f8fafc !important;
    font-weight: 900 !important;
    letter-spacing: -0.03em;
}

p, label {
    color: #e5e7eb !important;
}

/* FIX SELECTBOX / DROPDOWN */
div[data-baseweb="select"] > div {
    background-color: #f8fafc !important;
    border-radius: 12px !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color: #111827 !important;
}

div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] div {
    background-color: #ffffff !important;
    color: #111827 !important;
}

div[data-baseweb="popover"] li {
    color: #111827 !important;
}

input {
    color: #111827 !important;
}

textarea {
    color: #111827 !important;
}

/* BRAND */
.brand-box {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 18px 8px 22px 8px;
    border-bottom: 1px solid rgba(148,163,184,0.15);
    margin-bottom: 18px;
}

.brand-logo {
    width: 52px;
    height: 52px;
    border-radius: 18px;
    background: linear-gradient(135deg, #16a34a, #22c55e);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    box-shadow: 0 0 30px rgba(34,197,94,0.35);
}

.brand-title {
    font-size: 23px;
    font-weight: 950;
    color: white;
    line-height: 1;
}

.brand-subtitle {
    color: #22c55e;
    font-weight: 900;
    font-size: 13px;
    letter-spacing: 0.08em;
    margin-top: 5px;
}

.league-box {
    background: linear-gradient(135deg, rgba(34,197,94,0.12), rgba(59,130,246,0.10));
    border: 1px solid rgba(34,197,94,0.28);
    border-radius: 20px;
    padding: 16px;
    margin-bottom: 18px;
}

.league-small {
    color: #94a3b8;
    font-size: 11px;
    font-weight: 900;
    letter-spacing: 0.12em;
}

.league-name {
    color: #22c55e;
    font-size: 22px;
    font-weight: 950;
    margin-top: 4px;
}

.league-code {
    color: #cbd5e1;
    font-size: 13px;
    margin-top: 4px;
}

/* HERO */
.hero-card {
    background: linear-gradient(135deg, rgba(15,23,42,0.94), rgba(30,41,59,0.75));
    border: 1px solid rgba(148,163,184,0.22);
    border-radius: 26px;
    padding: 28px;
    margin-bottom: 20px;
    box-shadow: 0 22px 60px rgba(0,0,0,0.35);
}

.hero-title {
    font-size: 46px;
    font-weight: 950;
    color: #ffffff;
    letter-spacing: -0.05em;
}

.hero-subtitle {
    color: #cbd5e1;
    font-size: 15px;
    font-weight: 650;
}

/* CARDS */
.card {
    background: linear-gradient(135deg, rgba(15,23,42,0.92), rgba(17,24,39,0.78));
    border: 1px solid rgba(148,163,184,0.20);
    border-radius: 24px;
    padding: 20px;
    box-shadow: 0 18px 48px rgba(0,0,0,0.28);
    margin-bottom: 16px;
}

.card-green {
    border-color: rgba(34,197,94,0.35);
    background: linear-gradient(135deg, rgba(34,197,94,0.13), rgba(15,23,42,0.86));
}

.card-blue {
    border-color: rgba(59,130,246,0.35);
    background: linear-gradient(135deg, rgba(59,130,246,0.13), rgba(15,23,42,0.86));
}

.card-purple {
    border-color: rgba(168,85,247,0.35);
    background: linear-gradient(135deg, rgba(168,85,247,0.13), rgba(15,23,42,0.86));
}

.section-label {
    color: #22c55e;
    font-size: 14px;
    font-weight: 950;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 12px;
}

.stat-card {
    min-height: 105px;
    padding: 18px;
    border-radius: 22px;
    border: 1px solid rgba(148,163,184,0.18);
    background: linear-gradient(135deg, rgba(15,23,42,0.88), rgba(30,41,59,0.62));
    box-shadow: 0 14px 35px rgba(0,0,0,0.24);
}

.stat-title {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.stat-value {
    color: #ffffff;
    font-size: 32px;
    font-weight: 950;
    line-height: 1.1;
}

.stat-subtitle {
    color: #cbd5e1;
    font-size: 13px;
}

/* PLAYER */
.player-title {
    font-size: 40px;
    font-weight: 950;
    color: #ffffff;
    letter-spacing: -0.05em;
    line-height: 1;
    margin-bottom: 8px;
}

.player-sub {
    color: #cbd5e1;
    font-weight: 750;
    margin-bottom: 12px;
}

.role-badge {
    display: inline-block;
    padding: 8px 13px;
    border-radius: 999px;
    background: rgba(34,197,94,0.14);
    border: 1px solid rgba(34,197,94,0.35);
    color: #86efac;
    font-weight: 900;
    margin-right: 8px;
    margin-top: 8px;
    font-size: 13px;
}

.badge-blue {
    background: rgba(59,130,246,0.14);
    border-color: rgba(59,130,246,0.35);
    color: #bfdbfe;
}

.badge-yellow {
    background: rgba(245,158,11,0.16);
    border-color: rgba(245,158,11,0.36);
    color: #fde68a;
}

.badge-red {
    background: rgba(239,68,68,0.16);
    border-color: rgba(239,68,68,0.36);
    color: #fecaca;
}

.price-panel {
    background:
        radial-gradient(circle at top, rgba(250,204,21,0.22), transparent 38%),
        linear-gradient(135deg, rgba(15,23,42,0.96), rgba(30,41,59,0.88));
    border: 1px solid rgba(250,204,21,0.38);
    border-radius: 26px;
    padding: 28px;
    text-align: center;
    box-shadow: 0 18px 50px rgba(250,204,21,0.10);
}

.price-label {
    color: #cbd5e1;
    font-size: 12px;
    text-transform: uppercase;
    font-weight: 950;
    letter-spacing: 0.08em;
}

.price-number {
    color: #facc15;
    font-size: 82px;
    font-weight: 950;
    line-height: 0.95;
    text-shadow: 0 0 25px rgba(250,204,21,0.25);
}

.price-credit {
    color: #facc15;
    font-size: 20px;
    font-weight: 900;
    margin-bottom: 16px;
}

/* PLAYER DB CARD */
.player-card {
    background: linear-gradient(135deg, rgba(15,23,42,0.92), rgba(30,41,59,0.70));
    border: 1px solid rgba(148,163,184,0.20);
    border-radius: 22px;
    padding: 16px;
    margin-bottom: 12px;
    transition: 0.18s ease;
}

.player-card:hover {
    border-color: rgba(34,197,94,0.55);
    transform: translateY(-2px);
    box-shadow: 0 16px 40px rgba(34,197,94,0.10);
}

.player-card-name {
    color: white;
    font-size: 19px;
    font-weight: 950;
}

.player-card-sub {
    color: #94a3b8;
    font-size: 13px;
    margin-top: 3px;
}

.mini-stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-top: 12px;
}

.mini-stat {
    border-radius: 14px;
    padding: 10px;
    background: rgba(15,23,42,0.65);
    border: 1px solid rgba(148,163,184,0.14);
    text-align: center;
}

.mini-label {
    color: #94a3b8;
    font-size: 11px;
    font-weight: 850;
}

.mini-value {
    color: white;
    font-size: 18px;
    font-weight: 950;
}

/* RANK */
.ranking-row {
    display: grid;
    grid-template-columns: 30px 1fr 70px;
    align-items: center;
    gap: 10px;
    padding: 9px 0;
    border-bottom: 1px solid rgba(148,163,184,0.10);
}

.rank-num { color: #86efac; font-weight: 950; }
.rank-name { font-weight: 850; color: #f8fafc; }
.rank-credit { font-weight: 950; color: #ffffff; text-align: right; }

.progress-line {
    height: 4px;
    border-radius: 99px;
    margin-top: 5px;
    background: linear-gradient(90deg, #22c55e, #3b82f6, #a855f7);
}

.purchase-row {
    display: grid;
    grid-template-columns: 1fr 75px;
    gap: 8px;
    padding: 11px 0;
    border-bottom: 1px solid rgba(148,163,184,0.10);
}

.purchase-player { color: white; font-weight: 900; }
.purchase-team { color: #94a3b8; font-size: 12px; }
.purchase-price { color: #facc15; font-weight: 950; text-align: right; }

.stButton > button {
    border-radius: 14px !important;
    border: 1px solid rgba(148,163,184,0.25) !important;
    font-weight: 850 !important;
    min-height: 44px;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #16a34a, #22c55e) !important;
    color: white !important;
    border: 1px solid rgba(34,197,94,0.5) !important;
}

div[data-testid="stDataFrame"] {
    border-radius: 18px !important;
    overflow: hidden !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SUPABASE
# =========================
try:
    SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
    SUPABASE_KEY = st.secrets.get("SUPABASE_ANON_KEY", "")
except Exception:
    SUPABASE_URL = ""
    SUPABASE_KEY = ""

if not SUPABASE_URL:
    SUPABASE_URL = st.sidebar.text_input("Supabase URL")
if not SUPABASE_KEY:
    SUPABASE_KEY = st.sidebar.text_input("Supabase anon key", type="password")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.warning("Inserisci Supabase URL e Supabase anon key.")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================
# DB FUNCTIONS
# =========================
def get_lega_by_codice(codice):
    res = supabase.table("leghe").select("*").eq("codice_invito", codice).execute()
    return res.data[0] if res.data else None

def get_partecipanti(lega_id):
    return supabase.table("partecipanti").select("*").eq("lega_id", lega_id).order("nome_squadra").execute().data

def get_giocatori(query="", limit=100):
    q = supabase.table("giocatori").select("*").limit(limit)
    if query:
        q = q.ilike("nome", f"%{query}%")
    return q.execute().data

def get_giocatori_filtrati(query="", ruolo="", squadra="", limit=150):
    q = supabase.table("giocatori").select("*").limit(limit)
    if query:
        q = q.ilike("nome", f"%{query}%")
    if squadra and squadra != "Tutte":
        q = q.eq("squadra", squadra)
    data = q.execute().data
    if ruolo and ruolo != "Tutti":
        data = [g for g in data if ruolo.lower() in str(g.get("ruoli_mantra", "")).lower()]
    return data

def get_squadre():
    data = supabase.table("giocatori").select("squadra").execute().data
    squadre = sorted({d.get("squadra") for d in data if d.get("squadra")})
    return ["Tutte"] + squadre

def get_giocatore(id_giocatore):
    res = supabase.table("giocatori").select("*").eq("id_giocatore", id_giocatore).execute()
    return res.data[0] if res.data else None

def get_asta_attiva(lega_id):
    res = (
        supabase.table("asta_live")
        .select("*")
        .eq("lega_id", lega_id)
        .in_("stato", ["in_corso", "in_attesa"])
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    return res.data[0] if res.data else None

def crea_asta(lega_id, id_giocatore, prezzo_base=1):
    return supabase.table("asta_live").insert({
        "lega_id": lega_id,
        "id_giocatore": id_giocatore,
        "prezzo_corrente": prezzo_base,
        "partecipante_corrente": None,
        "stato": "in_corso",
        "timer_fine": (datetime.utcnow() + timedelta(seconds=30)).isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }).execute().data[0]

def rilancia(asta, partecipante_id, importo):
    partecipante = supabase.table("partecipanti").select("*").eq("id", partecipante_id).execute().data[0]
    if float(partecipante["crediti_residui"]) < float(importo):
        st.error("Crediti insufficienti.")
        return

    supabase.table("rilanci").insert({
        "lega_id": asta["lega_id"],
        "asta_id": asta["id"],
        "partecipante_id": partecipante_id,
        "id_giocatore": asta["id_giocatore"],
        "importo": importo
    }).execute()

    supabase.table("asta_live").update({
        "prezzo_corrente": importo,
        "partecipante_corrente": partecipante_id,
        "timer_fine": (datetime.utcnow() + timedelta(seconds=20)).isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }).eq("id", asta["id"]).execute()

def giocatore_gia_acquistato(lega_id, id_giocatore):
    res = supabase.table("rose").select("*").eq("lega_id", lega_id).eq("id_giocatore", id_giocatore).execute()
    return len(res.data) > 0

def assegna_giocatore(asta):
    if not asta.get("partecipante_corrente"):
        st.error("Nessuna offerta presente.")
        return

    lega_id = asta["lega_id"]
    id_giocatore = asta["id_giocatore"]
    partecipante_id = asta["partecipante_corrente"]
    prezzo = float(asta["prezzo_corrente"])

    if giocatore_gia_acquistato(lega_id, id_giocatore):
        st.error("Giocatore già acquistato.")
        return

    giocatore = get_giocatore(id_giocatore)
    partecipante = supabase.table("partecipanti").select("*").eq("id", partecipante_id).execute().data[0]
    nuovi_crediti = float(partecipante["crediti_residui"]) - prezzo

    if nuovi_crediti < 0:
        st.error("Crediti insufficienti.")
        return

    supabase.table("rose").insert({
        "lega_id": lega_id,
        "partecipante_id": partecipante_id,
        "id_giocatore": id_giocatore,
        "prezzo_acquisto": prezzo,
        "nome_giocatore": giocatore.get("nome"),
        "squadra_reale": giocatore.get("squadra"),
        "ruoli_mantra": giocatore.get("ruoli_mantra")
    }).execute()

    supabase.table("partecipanti").update({"crediti_residui": nuovi_crediti}).eq("id", partecipante_id).execute()
    supabase.table("asta_live").update({"stato": "chiusa", "updated_at": datetime.utcnow().isoformat()}).eq("id", asta["id"]).execute()

def annulla_asta(asta):
    supabase.table("asta_live").update({"stato": "annullata", "updated_at": datetime.utcnow().isoformat()}).eq("id", asta["id"]).execute()

def get_rosa(lega_id):
    return supabase.table("rose").select("*").eq("lega_id", lega_id).order("created_at").execute().data

def get_ultimi_acquisti(lega_id, limit=5):
    return (
        supabase.table("rose")
        .select("*, partecipanti(nome_squadra, nome_presidente)")
        .eq("lega_id", lega_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
        .data
    )

def get_rilanci(asta_id):
    return (
        supabase.table("rilanci")
        .select("*, partecipanti(nome_squadra, nome_presidente)")
        .eq("asta_id", asta_id)
        .order("created_at", desc=True)
        .limit(20)
        .execute()
        .data
    )

def reset_lega_totale(lega_id, budget=600):
    supabase.table("rilanci").delete().eq("lega_id", lega_id).execute()
    supabase.table("rose").delete().eq("lega_id", lega_id).execute()
    supabase.table("asta_live").delete().eq("lega_id", lega_id).execute()
    supabase.table("offerte").delete().eq("lega_id", lega_id).execute()
    supabase.table("partecipanti").update({"crediti_residui": budget}).eq("lega_id", lega_id).execute()

def get_commento_giocatore(lega_id, id_giocatore):
    res = supabase.table("commenti_giocatori").select("*").eq("lega_id", lega_id).eq("id_giocatore", id_giocatore).execute()
    return res.data[0] if res.data else None

def salva_commento_giocatore(lega_id, id_giocatore, commento, fascia, priorita, prezzo_massimo, voto_personale):
    dati = {
        "lega_id": lega_id,
        "id_giocatore": id_giocatore,
        "commento": commento,
        "fascia": fascia,
        "priorita": priorita,
        "prezzo_massimo": prezzo_massimo,
        "voto_personale": voto_personale,
        "updated_at": datetime.utcnow().isoformat()
    }
    esistente = get_commento_giocatore(lega_id, id_giocatore)
    if esistente:
        supabase.table("commenti_giocatori").update(dati).eq("id", esistente["id"]).execute()
    else:
        supabase.table("commenti_giocatori").insert(dati).execute()

def get_tutti_commenti(lega_id):
    return (
        supabase.table("commenti_giocatori")
        .select("*, giocatori(nome, squadra, ruoli_mantra, fanta_media, media_voto, quotazione_attuale, quotazione_attuale_mantra)")
        .eq("lega_id", lega_id)
        .order("updated_at", desc=True)
        .execute()
        .data
    )

# =========================
# UI FUNCTIONS
# =========================
def safe_num(value, default=0):
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default

def stat_card(title, value, subtitle="", color_class=""):
    st.markdown(f"""
    <div class="stat-card {color_class}">
        <div class="stat-title">{title}</div>
        <div class="stat-value">{value}</div>
        <div class="stat-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def sidebar_brand(lega):
    st.sidebar.markdown(f"""
    <div class="brand-box">
        <div class="brand-logo">⚽</div>
        <div>
            <div class="brand-title">FANTAMANTRA</div>
            <div class="brand-subtitle">ASTA LIVE</div>
        </div>
    </div>
    <div class="league-box">
        <div class="league-small">LEGA</div>
        <div class="league-name">{lega.get("nome")}</div>
        <div class="league-code">Codice: {lega.get("codice_invito")}</div>
    </div>
    """, unsafe_allow_html=True)

def player_header(g, commento=None):
    fascia = commento.get("fascia") if commento else "Da valutare"
    prezzo = commento.get("prezzo_massimo") if commento else "-"
    st.markdown(f"""
    <div class="card card-green">
        <div class="player-title">{g.get("nome")}</div>
        <div class="player-sub">🏟️ {g.get("squadra")} · 🎯 {g.get("ruoli_mantra")} · Ruolo classico: {g.get("ruolo_classico", "-")}</div>
        <span class="role-badge">MV {g.get("media_voto")}</span>
        <span class="role-badge">FM {g.get("fanta_media")}</span>
        <span class="role-badge badge-blue">Gol {g.get("gol_fatti")}</span>
        <span class="role-badge badge-blue">Assist {g.get("assist")}</span>
        <span class="role-badge badge-yellow">Q {g.get("quotazione_attuale")}</span>
        <span class="role-badge badge-yellow">Q Mantra {g.get("quotazione_attuale_mantra")}</span>
        <span class="role-badge badge-red">Fascia: {fascia}</span>
        <span class="role-badge badge-yellow">Prezzo max: {prezzo}</span>
    </div>
    """, unsafe_allow_html=True)

def player_card(g):
    st.markdown(f"""
    <div class="player-card">
        <div class="player-card-name">{g.get("nome")}</div>
        <div class="player-card-sub">🏟️ {g.get("squadra")} · 🎯 {g.get("ruoli_mantra")}</div>
        <div class="mini-stat-grid">
            <div class="mini-stat"><div class="mini-label">MV</div><div class="mini-value">{g.get("media_voto")}</div></div>
            <div class="mini-stat"><div class="mini-label">FM</div><div class="mini-value">{g.get("fanta_media")}</div></div>
            <div class="mini-stat"><div class="mini-label">GOL</div><div class="mini-value">{g.get("gol_fatti")}</div></div>
            <div class="mini-stat"><div class="mini-label">ASSIST</div><div class="mini-value">{g.get("assist")}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# SESSION
# =========================
if "lega" not in st.session_state:
    st.session_state.lega = None
if "partecipante" not in st.session_state:
    st.session_state.partecipante = None
if "selected_player_id" not in st.session_state:
    st.session_state.selected_player_id = None

# =========================
# LOGIN
# =========================
st.markdown("""
<div class="hero-card">
    <div class="hero-title">🏆 FantaMantra Asta Live</div>
    <div class="hero-subtitle">Asta, database, scouting e pagine giocatore in stile FantaLab.</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.lega is None:
    st.subheader("Entra nella lega")
    codice = st.text_input("Codice invito lega", value="Scanzano").strip()
    if st.button("Entra", type="primary"):
        lega = get_lega_by_codice(codice)
        if lega:
            st.session_state.lega = lega
            st.rerun()
        else:
            st.error("Codice lega non trovato.")
    st.stop()

lega = st.session_state.lega
sidebar_brand(lega)

partecipanti = get_partecipanti(lega["id"])

if st.session_state.partecipante is None:
    st.subheader("Scegli la tua squadra")
    labels = [f"{p['nome_squadra']} - {p['nome_presidente']}" for p in partecipanti]
    selected = st.selectbox("Squadra", labels)
    if st.button("Conferma squadra", type="primary"):
        idx = labels.index(selected)
        st.session_state.partecipante = partecipanti[idx]
        st.rerun()
    st.stop()

partecipante = st.session_state.partecipante
st.sidebar.info(f"Sei: {partecipante['nome_squadra']}")

if st.sidebar.button("Cambia squadra"):
    st.session_state.partecipante = None
    st.rerun()

pagina = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Sala asta",
        "Chiama giocatore",
        "Database giocatori",
        "Pagina giocatore",
        "Scouting / Commenti",
        "Partecipanti",
        "Rose",
        "Admin / Reset"
    ]
)

if st.sidebar.button("Aggiorna"):
    st.rerun()

# =========================
# DASHBOARD
# =========================
if pagina == "Dashboard":
    st.header("🏆 Dashboard Lega")

    partecipanti_now = get_partecipanti(lega["id"])
    rosa_now = get_rosa(lega["id"])
    ultimi = get_ultimi_acquisti(lega["id"], 5)
    crediti_totali = sum(safe_num(p.get("crediti_residui")) for p in partecipanti_now)
    assegnati = len(rosa_now)
    ultimo_nome = ultimi[0].get("nome_giocatore") if ultimi else "Nessuno"

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: stat_card("Partecipanti", f"{len(partecipanti_now)}/10", "iscritti")
    with c2: stat_card("Budget iniziale", "600", "crediti")
    with c3: stat_card("Giocatori assegnati", f"{assegnati}/663", "totale")
    with c4: stat_card("Crediti residui", f"{int(crediti_totali)}", "totali")
    with c5: stat_card("Ultimo acquisto", ultimo_nome, "-")

    st.write("")
    col_left, col_right = st.columns([1.4, 1])

    with col_left:
        asta = get_asta_attiva(lega["id"])
        if asta:
            g = get_giocatore(asta["id_giocatore"])
            migliore_nome = "Nessuna offerta"
            if asta.get("partecipante_corrente"):
                migliore = [p for p in partecipanti_now if p["id"] == asta["partecipante_corrente"]]
                if migliore:
                    migliore_nome = migliore[0]["nome_squadra"]
            player_header(g)
            st.markdown(f"""
            <div class="price-panel">
                <div class="price-label">Prezzo attuale</div>
                <div class="price-number">{asta.get("prezzo_corrente")}</div>
                <div class="price-credit">crediti</div>
                <div class="player-sub">Miglior offerente: <b>{migliore_nome}</b></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card">
                <div class="section-label">Giocatore in asta</div>
                <div class="player-title">Nessun giocatore chiamato</div>
                <div class="player-sub">Vai su “Chiama giocatore” per iniziare.</div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="card"><div class="section-label">Classifica crediti residui</div>', unsafe_allow_html=True)
        for i, p in enumerate(sorted(partecipanti_now, key=lambda x: safe_num(x.get("crediti_residui")), reverse=True), start=1):
            cred = int(safe_num(p.get("crediti_residui")))
            width = max(8, min(100, cred / 600 * 100))
            st.markdown(f"""
            <div class="ranking-row">
                <div class="rank-num">{i}</div>
                <div>
                    <div class="rank-name">{p.get("nome_squadra")}</div>
                    <div class="progress-line" style="width:{width}%;"></div>
                </div>
                <div class="rank-credit">{cred}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="card"><div class="section-label">Ultimi acquisti</div>', unsafe_allow_html=True)
        if ultimi:
            for u in ultimi:
                p = u.get("partecipanti") or {}
                st.markdown(f"""
                <div class="purchase-row">
                    <div>
                        <div class="purchase-player">{u.get("nome_giocatore")}</div>
                        <div class="purchase-team">{p.get("nome_squadra")} · {u.get("ruoli_mantra")}</div>
                    </div>
                    <div class="purchase-price">{u.get("prezzo_acquisto")}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("Nessun acquisto.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="card"><div class="section-label">Scouting rapido</div>', unsafe_allow_html=True)
        commenti = get_tutti_commenti(lega["id"])[:4]
        if commenti:
            for c in commenti:
                g = c.get("giocatori") or {}
                stars = "★" * int(round(safe_num(c.get("voto_personale"), 0) / 2))
                st.markdown(f"""
                <div class="scout-card">
                    <div class="scout-name">{g.get("nome")}</div>
                    <div class="scout-sub">{g.get("squadra")} · {g.get("ruoli_mantra")}</div>
                    <div class="stars">{stars}</div>
                    <span class="role-badge">{c.get("fascia")}</span>
                    <span class="role-badge badge-yellow">Max {c.get("prezzo_massimo")}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("Nessun commento scouting salvato.")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# SALA ASTA
# =========================
elif pagina == "Sala asta":
    st.header("🔥 Sala asta live")
    asta = get_asta_attiva(lega["id"])

    if not asta:
        st.info("Nessun giocatore attualmente all'asta.")
    else:
        g = get_giocatore(asta["id_giocatore"])
        partecipanti_now = get_partecipanti(lega["id"])
        nome_migliore = "Nessuna offerta"
        if asta.get("partecipante_corrente"):
            migliore = [p for p in partecipanti_now if p["id"] == asta["partecipante_corrente"]]
            if migliore:
                nome_migliore = migliore[0]["nome_squadra"]

        col1, col2 = st.columns([1.6, 1])
        with col1:
            player_header(g, get_commento_giocatore(lega["id"], g["id_giocatore"]))
        with col2:
            st.markdown(f"""
            <div class="price-panel">
                <div class="price-label">Prezzo corrente</div>
                <div class="price-number">{asta["prezzo_corrente"]}</div>
                <div class="price-credit">crediti</div>
                <div class="player-sub">Miglior offerente: <b>{nome_migliore}</b></div>
            </div>
            """, unsafe_allow_html=True)

        prezzo_corrente = float(asta["prezzo_corrente"])
        minimo = prezzo_corrente + 1

        st.subheader("Rilancia")
        cols = st.columns(5)
        increments = [1, 5, 10, 20, 50]
        for col, inc in zip(cols, increments):
            with col:
                if st.button(f"+{inc} → {prezzo_corrente + inc}"):
                    rilancia(asta, partecipante["id"], prezzo_corrente + inc)
                    st.rerun()

        col_m1, col_m2 = st.columns([2, 1])
        with col_m1:
            offerta_custom = st.number_input("Offerta manuale", min_value=float(minimo), step=1.0)
        with col_m2:
            if st.button("Rilancia manualmente"):
                rilancia(asta, partecipante["id"], offerta_custom)
                st.rerun()

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Assegna al miglior offerente", type="primary"):
                assegna_giocatore(asta)
                st.rerun()
        with c2:
            if st.button("❌ Annulla asta"):
                annulla_asta(asta)
                st.rerun()

        st.subheader("Ultimi rilanci")
        rilanci = get_rilanci(asta["id"])
        if rilanci:
            rows = []
            for r in rilanci:
                p = r.get("partecipanti") or {}
                rows.append({
                    "squadra": p.get("nome_squadra"),
                    "presidente": p.get("nome_presidente"),
                    "importo": r.get("importo"),
                    "orario": r.get("created_at")
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
        else:
            st.info("Ancora nessun rilancio.")

# =========================
# CHIAMA GIOCATORE
# =========================
elif pagina == "Chiama giocatore":
    st.header("📣 Chiama un giocatore")
    asta = get_asta_attiva(lega["id"])

    if asta:
        st.warning("C'è già un'asta attiva. Chiudila o annullala prima.")
    else:
        search = st.text_input("Cerca giocatore per nome")
        giocatori = get_giocatori(search, limit=100)

        if giocatori:
            options = [f"{g['id_giocatore']} - {g['nome']} | {g.get('squadra')} | {g.get('ruoli_mantra')}" for g in giocatori]
            scelta = st.selectbox("Seleziona giocatore da chiamare", options)
            id_giocatore = int(scelta.split(" - ")[0])
            g = get_giocatore(id_giocatore)
            player_header(g, get_commento_giocatore(lega["id"], id_giocatore))

            prezzo_base = st.number_input("Prezzo base", min_value=1.0, value=1.0, step=1.0)

            if giocatore_gia_acquistato(lega["id"], id_giocatore):
                st.error("Questo giocatore è già stato acquistato.")
            else:
                if st.button("🚀 Avvia asta", type="primary"):
                    crea_asta(lega["id"], id_giocatore, prezzo_base)
                    st.success("Asta avviata.")
                    st.rerun()
        else:
            st.info("Nessun giocatore trovato.")

# =========================
# DATABASE GIOCATORI COLORATO
# =========================
elif pagina == "Database giocatori":
    st.header("📋 Database giocatori")

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        search = st.text_input("Cerca nome")
    with col_f2:
        ruolo = st.selectbox("Filtro ruolo Mantra", ["Tutti", "Por", "Dc", "Ds", "Dd", "E", "M", "C", "T", "W", "A", "Pc"])
    with col_f3:
        squadra = st.selectbox("Filtro squadra", get_squadre())

    giocatori = get_giocatori_filtrati(search, ruolo, squadra, limit=150)

    if giocatori:
        st.caption(f"{len(giocatori)} giocatori trovati")

        for i in range(0, len(giocatori), 3):
            cols = st.columns(3)
            for col, g in zip(cols, giocatori[i:i+3]):
                with col:
                    player_card(g)
                    if st.button(f"Apri scheda", key=f"open_{g['id_giocatore']}"):
                        st.session_state.selected_player_id = g["id_giocatore"]
                        st.rerun()
    else:
        st.info("Nessun giocatore trovato.")

# =========================
# PAGINA GIOCATORE
# =========================
elif pagina == "Pagina giocatore":
    st.header("🧬 Pagina giocatore")

    search = st.text_input("Cerca giocatore")
    giocatori = get_giocatori(search, limit=100)

    if giocatori:
        options = [f"{g['id_giocatore']} - {g['nome']} | {g.get('squadra')} | {g.get('ruoli_mantra')}" for g in giocatori]
        default_index = 0
        if st.session_state.selected_player_id:
            for idx, label in enumerate(options):
                if label.startswith(str(st.session_state.selected_player_id) + " - "):
                    default_index = idx
                    break

        scelta = st.selectbox("Seleziona giocatore", options, index=default_index)
        id_giocatore = int(scelta.split(" - ")[0])
        st.session_state.selected_player_id = id_giocatore
        g = get_giocatore(id_giocatore)
        commento_old = get_commento_giocatore(lega["id"], id_giocatore)

        player_header(g, commento_old)

        col1, col2, col3, col4 = st.columns(4)
        with col1: stat_card("Partite a voto", g.get("partite_a_voto"), "presenze utili")
        with col2: stat_card("Media voto", g.get("media_voto"), "rendimento puro")
        with col3: stat_card("Fanta media", g.get("fanta_media"), "bonus/malus")
        with col4: stat_card("Quotazione", g.get("quotazione_attuale"), "attuale")

        col_a, col_b = st.columns([1.2, 1])

        with col_a:
            st.markdown('<div class="card"><div class="section-label">Statistiche complete</div>', unsafe_allow_html=True)
            stats = {
                "Gol fatti": g.get("gol_fatti"),
                "Gol subiti": g.get("gol_subiti"),
                "Rigori parati": g.get("rigori_parati"),
                "Rigori calciati": g.get("rigori_calciati"),
                "Rigori segnati": g.get("rigori_segnati"),
                "Rigori sbagliati": g.get("rigori_sbagliati"),
                "Assist": g.get("assist"),
                "Ammonizioni": g.get("ammonizioni"),
                "Espulsioni": g.get("espulsioni"),
                "Autogol": g.get("autogol"),
                "Quotazione iniziale": g.get("quotazione_iniziale"),
                "Differenza quotazione": g.get("differenza_quotazione"),
                "Quotazione attuale Mantra": g.get("quotazione_attuale_mantra"),
                "Quotazione iniziale Mantra": g.get("quotazione_iniziale_mantra"),
                "Differenza Mantra": g.get("differenza_quotazione_mantra"),
            }
            st.dataframe(pd.DataFrame([stats]).T.rename(columns={0: "Valore"}), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_b:
            st.markdown('<div class="card card-purple"><div class="section-label">Scouting personale</div>', unsafe_allow_html=True)

            fascia_default = commento_old.get("fascia") if commento_old else "Da valutare"
            priorita_default = commento_old.get("priorita") if commento_old else "Media"

            fasce = ["Top", "Semi-top", "Titolare utile", "Scommessa", "Riserva", "Da evitare", "Da valutare"]
            priorita_opzioni = ["Altissima", "Alta", "Media", "Bassa", "No"]

            fascia = st.selectbox("Fascia", fasce, index=fasce.index(fascia_default) if fascia_default in fasce else fasce.index("Da valutare"))
            priorita = st.selectbox("Priorità", priorita_opzioni, index=priorita_opzioni.index(priorita_default) if priorita_default in priorita_opzioni else priorita_opzioni.index("Media"))

            prezzo_massimo = st.number_input(
                "Prezzo massimo",
                min_value=0.0,
                value=float(commento_old.get("prezzo_massimo") or 0) if commento_old else 0.0,
                step=1.0
            )

            voto_personale = st.number_input(
                "Voto scouting",
                min_value=0.0,
                max_value=10.0,
                value=float(commento_old.get("voto_personale") or 6) if commento_old else 6.0,
                step=0.5
            )

            commento = st.text_area(
                "Commento",
                value=commento_old.get("commento") if commento_old else "",
                height=170
            )

            if st.button("💾 Salva scouting", type="primary"):
                salva_commento_giocatore(lega["id"], id_giocatore, commento, fascia, priorita, prezzo_massimo, voto_personale)
                st.success("Scouting salvato.")
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

# =========================
# SCOUTING LISTA
# =========================
elif pagina == "Scouting / Commenti":
    st.header("🧠 Scouting / Commenti")
    commenti = get_tutti_commenti(lega["id"])

    if commenti:
        rows = []
        for c in commenti:
            g = c.get("giocatori") or {}
            rows.append({
                "nome": g.get("nome"),
                "squadra": g.get("squadra"),
                "ruoli": g.get("ruoli_mantra"),
                "fanta_media": g.get("fanta_media"),
                "quotazione": g.get("quotazione_attuale"),
                "fascia": c.get("fascia"),
                "priorita": c.get("priorita"),
                "prezzo_massimo": c.get("prezzo_massimo"),
                "voto_personale": c.get("voto_personale"),
                "commento": c.get("commento")
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
    else:
        st.info("Ancora nessun commento salvato. Vai su Pagina giocatore per crearli.")

# =========================
# PARTECIPANTI
# =========================
elif pagina == "Partecipanti":
    st.header("👥 Partecipanti")
    st.dataframe(pd.DataFrame(get_partecipanti(lega["id"])), use_container_width=True)

# =========================
# ROSE
# =========================
elif pagina == "Rose":
    st.header("🌹 Rose")
    rosa = get_rosa(lega["id"])
    partecipanti_now = get_partecipanti(lega["id"])

    if not rosa:
        st.info("Ancora nessun giocatore acquistato.")
    else:
        df_rosa = pd.DataFrame(rosa)
        for p in partecipanti_now:
            st.markdown(f"""
            <div class="card">
                <div class="section-label">{p['nome_squadra']}</div>
                <div class="player-sub">Crediti residui: <b>{p['crediti_residui']}</b></div>
            </div>
            """, unsafe_allow_html=True)
            sub = df_rosa[df_rosa["partecipante_id"] == p["id"]]
            if sub.empty:
                st.caption("Nessun acquisto.")
            else:
                st.dataframe(sub[["nome_giocatore", "squadra_reale", "ruoli_mantra", "prezzo_acquisto"]], use_container_width=True)

# =========================
# ADMIN RESET
# =========================
elif pagina == "Admin / Reset":
    st.header("🧨 Admin / Reset")
    st.markdown("""
    <div class="card card-purple">
        <div class="section-label">Reset prove</div>
        Cancella rose, rilanci, aste attive e offerte. Non cancella giocatori, statistiche, partecipanti e scouting.
    </div>
    """, unsafe_allow_html=True)

    budget_reset = st.number_input("Budget a cui riportare tutti", min_value=1.0, value=600.0, step=1.0)
    conferma = st.text_input("Per confermare scrivi RESET")

    if conferma == "RESET":
        if st.button("🧨 RESETTA TUTTA L'ASTA", type="primary"):
            reset_lega_totale(lega["id"], budget_reset)
            st.success("Reset completato.")
            st.rerun()
    else:
        st.info("Scrivi RESET per sbloccare il pulsante.")
