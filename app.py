
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
# CSS PREMIUM UI
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(34,197,94,0.16), transparent 32%),
            radial-gradient(circle at top right, rgba(168,85,247,0.14), transparent 34%),
            linear-gradient(135deg, #020617 0%, #0f172a 48%, #111827 100%);
        color: #f8fafc;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(2,6,23,0.98), rgba(15,23,42,0.98));
        border-right: 1px solid rgba(148,163,184,0.18);
    }

    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 900 !important;
        letter-spacing: -0.03em;
    }

    p, label, span, div { color: #e5e7eb; }

    .hero-card {
        background: linear-gradient(135deg, rgba(15,23,42,0.92), rgba(30,41,59,0.75));
        border: 1px solid rgba(148,163,184,0.20);
        border-radius: 24px;
        padding: 26px 28px;
        margin-bottom: 18px;
        box-shadow: 0 18px 50px rgba(0,0,0,0.32);
    }

    .hero-title {
        font-size: 44px;
        font-weight: 950;
        color: #ffffff;
        letter-spacing: -0.05em;
        margin-bottom: 4px;
    }

    .hero-subtitle {
        color: #cbd5e1;
        font-size: 15px;
        font-weight: 600;
    }

    .brand-box {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 18px 10px 24px 10px;
        border-bottom: 1px solid rgba(148,163,184,0.16);
        margin-bottom: 16px;
    }

    .brand-logo {
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 16px;
        background: linear-gradient(135deg, #16a34a, #22c55e);
        box-shadow: 0 0 28px rgba(34,197,94,0.35);
        font-size: 28px;
    }

    .brand-title {
        font-size: 22px;
        font-weight: 900;
        color: white;
        line-height: 1;
    }

    .brand-subtitle {
        font-size: 13px;
        font-weight: 800;
        color: #22c55e;
        margin-top: 4px;
        letter-spacing: 0.08em;
    }

    .league-box {
        background: linear-gradient(135deg, rgba(34,197,94,0.12), rgba(59,130,246,0.10));
        border: 1px solid rgba(34,197,94,0.25);
        border-radius: 18px;
        padding: 16px;
        margin: 8px 0 18px 0;
    }

    .league-small {
        color: #94a3b8;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.14em;
    }

    .league-name {
        color: #22c55e;
        font-size: 22px;
        font-weight: 900;
        margin-top: 4px;
    }

    .league-code {
        color: #cbd5e1;
        font-size: 13px;
        margin-top: 4px;
    }

    .premium-stat-card {
        display: flex;
        align-items: center;
        gap: 16px;
        min-height: 105px;
        padding: 18px;
        background: linear-gradient(135deg, rgba(15,23,42,0.86), rgba(30,41,59,0.62));
        border: 1px solid rgba(148,163,184,0.20);
        border-radius: 20px;
        box-shadow: 0 14px 35px rgba(0,0,0,0.22);
    }

    .stat-icon {
        font-size: 38px;
        filter: drop-shadow(0 0 15px rgba(34,197,94,0.25));
    }

    .stat-title {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .stat-value {
        color: #fff;
        font-size: 31px;
        font-weight: 950;
        line-height: 1.1;
    }

    .stat-subtitle {
        color: #cbd5e1;
        font-size: 13px;
        margin-top: 3px;
    }

    .auction-grid-card {
        background: linear-gradient(135deg, rgba(15,23,42,0.9), rgba(17,24,39,0.76));
        border: 1px solid rgba(148,163,184,0.22);
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 18px 48px rgba(0,0,0,0.30);
        margin-bottom: 16px;
    }

    .section-label {
        color: #22c55e;
        font-size: 14px;
        font-weight: 900;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 14px;
    }

    .player-name-big {
        font-size: 36px;
        font-weight: 950;
        color: #fff;
        letter-spacing: -0.04em;
        line-height: 1;
        margin-bottom: 8px;
    }

    .player-meta {
        color: #cbd5e1;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .pill {
        display: inline-block;
        background: rgba(34,197,94,0.13);
        color: #86efac;
        padding: 7px 12px;
        border-radius: 999px;
        margin-right: 8px;
        margin-top: 8px;
        border: 1px solid rgba(34,197,94,0.32);
        font-weight: 800;
        font-size: 13px;
    }

    .pill-blue {
        background: rgba(59,130,246,0.14);
        color: #bfdbfe;
        border-color: rgba(59,130,246,0.35);
    }

    .pill-yellow {
        background: rgba(245,158,11,0.15);
        color: #fde68a;
        border-color: rgba(245,158,11,0.36);
    }

    .price-panel {
        background:
            radial-gradient(circle at top, rgba(250,204,21,0.20), transparent 35%),
            linear-gradient(135deg, rgba(15,23,42,0.96), rgba(30,41,59,0.86));
        border: 1px solid rgba(250,204,21,0.36);
        border-radius: 24px;
        padding: 26px;
        text-align: center;
        box-shadow: 0 18px 44px rgba(250,204,21,0.10);
    }

    .price-label {
        color: #cbd5e1;
        font-size: 12px;
        text-transform: uppercase;
        font-weight: 900;
        letter-spacing: 0.08em;
    }

    .price-number {
        color: #facc15;
        font-size: 76px;
        font-weight: 950;
        line-height: 0.95;
        text-shadow: 0 0 25px rgba(250,204,21,0.22);
    }

    .price-credit {
        color: #facc15;
        font-size: 20px;
        font-weight: 900;
        margin-bottom: 18px;
    }

    .best-bidder {
        border-top: 1px solid rgba(148,163,184,0.20);
        padding-top: 18px;
        margin-top: 18px;
        font-size: 22px;
        font-weight: 950;
        color: #fff;
    }

    .ranking-row {
        display: grid;
        grid-template-columns: 30px 1fr 70px;
        align-items: center;
        gap: 10px;
        padding: 9px 0;
        border-bottom: 1px solid rgba(148,163,184,0.10);
    }

    .rank-num { color: #86efac; font-weight: 900; }
    .rank-name { font-weight: 800; color: #f8fafc; }
    .rank-credit { font-weight: 950; color: #ffffff; text-align: right; }

    .progress-line {
        height: 4px;
        border-radius: 99px;
        margin-top: 5px;
        background: linear-gradient(90deg, #22c55e, #3b82f6, #a855f7);
    }

    .purchase-row {
        display: grid;
        grid-template-columns: 1fr 70px;
        gap: 8px;
        padding: 11px 0;
        border-bottom: 1px solid rgba(148,163,184,0.10);
    }

    .purchase-player { color: white; font-weight: 850; }
    .purchase-team { color: #94a3b8; font-size: 12px; }
    .purchase-price { color: #facc15; font-weight: 950; text-align: right; }

    .scout-card {
        background: linear-gradient(135deg, rgba(15,23,42,0.92), rgba(30,41,59,0.68));
        border: 1px solid rgba(148,163,184,0.18);
        border-radius: 18px;
        padding: 16px;
        min-height: 122px;
        margin-bottom: 10px;
    }

    .scout-name { color: white; font-size: 17px; font-weight: 900; }
    .scout-sub { color: #94a3b8; font-size: 12px; margin-bottom: 8px; }
    .stars { color: #facc15; letter-spacing: 2px; font-size: 15px; }

    .danger-box {
        background: rgba(239,68,68,0.15);
        border: 1px solid rgba(239,68,68,0.45);
        border-radius: 18px;
        padding: 18px;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.08);
        padding: 18px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.12);
    }

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
</style>
""", unsafe_allow_html=True)

# =========================
# CONFIG SUPABASE
# =========================
try:
    SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
    SUPABASE_KEY = st.secrets.get("SUPABASE_ANON_KEY", "")
except Exception:
    SUPABASE_URL = ""
    SUPABASE_KEY = ""

st.sidebar.title("⚙️ Connessione")

if not SUPABASE_URL:
    SUPABASE_URL = st.sidebar.text_input("Supabase URL", type="default")

if not SUPABASE_KEY:
    SUPABASE_KEY = st.sidebar.text_input("Supabase anon key", type="password")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.warning("Inserisci Supabase URL e Supabase anon key nella sidebar.")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================
# FUNZIONI DATABASE
# =========================
def get_lega_by_codice(codice):
    res = supabase.table("leghe").select("*").eq("codice_invito", codice).execute()
    return res.data[0] if res.data else None

def get_partecipanti(lega_id):
    res = supabase.table("partecipanti").select("*").eq("lega_id", lega_id).order("nome_squadra").execute()
    return res.data

def get_giocatori(query="", limit=100):
    q = supabase.table("giocatori").select("*").limit(limit)
    if query:
        q = q.ilike("nome", f"%{query}%")
    res = q.execute()
    return res.data

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
    dati = {
        "lega_id": lega_id,
        "id_giocatore": id_giocatore,
        "prezzo_corrente": prezzo_base,
        "partecipante_corrente": None,
        "stato": "in_corso",
        "timer_fine": (datetime.utcnow() + timedelta(seconds=30)).isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    res = supabase.table("asta_live").insert(dati).execute()
    return res.data[0]

def rilancia(asta, partecipante_id, importo):
    asta_id = asta["id"]
    lega_id = asta["lega_id"]
    id_giocatore = asta["id_giocatore"]

    partecipante = supabase.table("partecipanti").select("*").eq("id", partecipante_id).execute().data[0]
    if float(partecipante["crediti_residui"]) < float(importo):
        st.error("Crediti insufficienti.")
        return

    supabase.table("rilanci").insert({
        "lega_id": lega_id,
        "asta_id": asta_id,
        "partecipante_id": partecipante_id,
        "id_giocatore": id_giocatore,
        "importo": importo
    }).execute()

    supabase.table("asta_live").update({
        "prezzo_corrente": importo,
        "partecipante_corrente": partecipante_id,
        "timer_fine": (datetime.utcnow() + timedelta(seconds=20)).isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }).eq("id", asta_id).execute()

def giocatore_gia_acquistato(lega_id, id_giocatore):
    res = (
        supabase.table("rose")
        .select("*")
        .eq("lega_id", lega_id)
        .eq("id_giocatore", id_giocatore)
        .execute()
    )
    return len(res.data) > 0

def assegna_giocatore(asta):
    if not asta.get("partecipante_corrente"):
        st.error("Nessuna offerta presente. Non puoi assegnare il giocatore.")
        return

    lega_id = asta["lega_id"]
    id_giocatore = asta["id_giocatore"]
    partecipante_id = asta["partecipante_corrente"]
    prezzo = float(asta["prezzo_corrente"])

    if giocatore_gia_acquistato(lega_id, id_giocatore):
        st.error("Questo giocatore è già stato acquistato.")
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

    supabase.table("partecipanti").update({
        "crediti_residui": nuovi_crediti
    }).eq("id", partecipante_id).execute()

    supabase.table("asta_live").update({
        "stato": "chiusa",
        "updated_at": datetime.utcnow().isoformat()
    }).eq("id", asta["id"]).execute()

    st.success(f"{giocatore.get('nome')} assegnato a {partecipante.get('nome_squadra')} per {prezzo} crediti.")

def annulla_asta(asta):
    supabase.table("asta_live").update({
        "stato": "annullata",
        "updated_at": datetime.utcnow().isoformat()
    }).eq("id", asta["id"]).execute()

def get_rosa(lega_id):
    res = (
        supabase.table("rose")
        .select("*")
        .eq("lega_id", lega_id)
        .order("created_at", desc=False)
        .execute()
    )
    return res.data

def get_ultimi_acquisti(lega_id, limit=5):
    res = (
        supabase.table("rose")
        .select("*, partecipanti(nome_squadra, nome_presidente)")
        .eq("lega_id", lega_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return res.data

def get_rilanci(asta_id):
    res = (
        supabase.table("rilanci")
        .select("*, partecipanti(nome_squadra, nome_presidente)")
        .eq("asta_id", asta_id)
        .order("created_at", desc=True)
        .limit(20)
        .execute()
    )
    return res.data

def reset_lega_totale(lega_id, budget=600):
    supabase.table("rilanci").delete().eq("lega_id", lega_id).execute()
    supabase.table("rose").delete().eq("lega_id", lega_id).execute()
    supabase.table("asta_live").delete().eq("lega_id", lega_id).execute()
    supabase.table("offerte").delete().eq("lega_id", lega_id).execute()
    supabase.table("partecipanti").update({
        "crediti_residui": budget
    }).eq("lega_id", lega_id).execute()

def get_commento_giocatore(lega_id, id_giocatore):
    res = (
        supabase.table("commenti_giocatori")
        .select("*")
        .eq("lega_id", lega_id)
        .eq("id_giocatore", id_giocatore)
        .execute()
    )
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
    res = (
        supabase.table("commenti_giocatori")
        .select("*, giocatori(nome, squadra, ruoli_mantra, fanta_media, quotazione_attuale, quotazione_attuale_mantra)")
        .eq("lega_id", lega_id)
        .order("updated_at", desc=True)
        .execute()
    )
    return res.data

# =========================
# FUNZIONI UI
# =========================
def safe_num(value, default=0):
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default

def render_stat_card(title, value, subtitle="", icon="📊", color="#22c55e"):
    st.markdown(f"""
    <div class="premium-stat-card">
        <div class="stat-icon" style="color:{color};">{icon}</div>
        <div>
            <div class="stat-title">{title}</div>
            <div class="stat-value">{value}</div>
            <div class="stat-subtitle">{subtitle}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar_brand(lega=None):
    codice = lega.get("codice_invito") if lega else "-"
    nome = lega.get("nome") if lega else "FantaMantra"
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
        <div class="league-name">{nome}</div>
        <div class="league-code">Codice: {codice}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# SESSIONE
# =========================
if "lega" not in st.session_state:
    st.session_state.lega = None

if "partecipante" not in st.session_state:
    st.session_state.partecipante = None

# =========================
# LOGIN LEGA
# =========================
st.markdown("""
<div class="hero-card">
    <div class="hero-title">🏆 Asta Scanzano</div>
    <div class="hero-subtitle">La tua asta. La tua lega. Il tuo FantaMantra.</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.lega is None:
    st.subheader("Entra nella lega")
    codice = st.text_input("Codice invito lega", value="Scanzano").strip()

    if st.button("Entra"):
        lega = get_lega_by_codice(codice)
        if lega:
            st.session_state.lega = lega
            st.rerun()
        else:
            st.error("Codice lega non trovato.")

    st.stop()

lega = st.session_state.lega

render_sidebar_brand(lega)

# =========================
# SCELTA PARTECIPANTE
# =========================
partecipanti = get_partecipanti(lega["id"])

if st.session_state.partecipante is None:
    st.subheader("Scegli la tua squadra")

    labels = [f"{p['nome_squadra']} - {p['nome_presidente']}" for p in partecipanti]
    selected = st.selectbox("Squadra", labels)

    if st.button("Conferma squadra"):
        idx = labels.index(selected)
        st.session_state.partecipante = partecipanti[idx]
        st.rerun()

    st.stop()

partecipante = st.session_state.partecipante

st.sidebar.info(f"Sei: {partecipante['nome_squadra']}")

if st.sidebar.button("Cambia squadra"):
    st.session_state.partecipante = None
    st.rerun()

# =========================
# MENU
# =========================
pagina = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Sala asta",
        "Chiama giocatore",
        "Scouting / Commenti",
        "Partecipanti",
        "Rose",
        "Database giocatori",
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
    with c1:
        render_stat_card("Partecipanti", f"{len(partecipanti_now)}/10", "iscritti", "👥", "#22c55e")
    with c2:
        render_stat_card("Budget iniziale", "600", "crediti", "💼", "#38bdf8")
    with c3:
        render_stat_card("Giocatori assegnati", f"{assegnati}/663", "totale", "👕", "#a855f7")
    with c4:
        render_stat_card("Crediti residui", f"{int(crediti_totali)}", "totali", "🪙", "#facc15")
    with c5:
        render_stat_card("Ultimo acquisto", ultimo_nome, "-", "📈", "#fb7185")

    st.write("")

    col_left, col_right = st.columns([1.45, 1])

    with col_left:
        asta = get_asta_attiva(lega["id"])
        if asta:
            giocatore = get_giocatore(asta["id_giocatore"])
            migliore_nome = "Nessuna offerta"
            if asta.get("partecipante_corrente"):
                migliore = [p for p in partecipanti_now if p["id"] == asta["partecipante_corrente"]]
                if migliore:
                    migliore_nome = migliore[0]["nome_squadra"]

            st.markdown(f"""
            <div class="auction-grid-card">
                <div class="section-label">● Giocatore in asta</div>
                <div class="player-name-big">{giocatore.get("nome")}</div>
                <div class="player-meta">🏟️ {giocatore.get("squadra")} · 🎯 {giocatore.get("ruoli_mantra")}</div>
                <span class="pill">MV {giocatore.get("media_voto")}</span>
                <span class="pill">FM {giocatore.get("fanta_media")}</span>
                <span class="pill pill-blue">Gol {giocatore.get("gol_fatti")}</span>
                <span class="pill pill-blue">Assist {giocatore.get("assist")}</span>
                <span class="pill pill-yellow">Quotazione {giocatore.get("quotazione_attuale")}</span>
                <br><br>
                <div class="price-panel">
                    <div class="price-label">Prezzo attuale</div>
                    <div class="price-number">{asta.get("prezzo_corrente")}</div>
                    <div class="price-credit">crediti</div>
                    <div class="best-bidder">Miglior offerente: {migliore_nome}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="auction-grid-card">
                <div class="section-label">● Giocatore in asta</div>
                <div class="player-name-big">Nessun giocatore chiamato</div>
                <div class="player-meta">Vai su “Chiama giocatore” per iniziare una nuova asta.</div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="auction-grid-card"><div class="section-label">Classifica crediti residui</div>', unsafe_allow_html=True)
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
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown('<div class="auction-grid-card"><div class="section-label">Ultimi acquisti</div>', unsafe_allow_html=True)
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
            st.caption("Nessun acquisto ancora registrato.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="auction-grid-card"><div class="section-label">Scouting rapido</div>', unsafe_allow_html=True)
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
                    <span class="pill">{c.get("fascia")}</span>
                    <span class="pill pill-yellow">Max {c.get("prezzo_massimo")}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("Nessun commento scouting salvato.")
        st.markdown('</div>', unsafe_allow_html=True)

# =========================
# SALA ASTA
# =========================
elif pagina == "Sala asta":
    st.header("🔥 Sala asta live")

    asta = get_asta_attiva(lega["id"])

    if not asta:
        st.info("Nessun giocatore attualmente all'asta.")
    else:
        giocatore = get_giocatore(asta["id_giocatore"])

        partecipanti = get_partecipanti(lega["id"])
        nome_migliore = "Nessuna offerta"
        if asta.get("partecipante_corrente"):
            migliore = [p for p in partecipanti if p["id"] == asta["partecipante_corrente"]]
            if migliore:
                nome_migliore = migliore[0]["nome_squadra"]

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"""
            <div class="auction-grid-card">
                <div class="section-label">● Giocatore in asta</div>
                <div class="player-name-big">{giocatore.get('nome')}</div>
                <div class="player-meta">🏟️ {giocatore.get('squadra')} · 🎯 {giocatore.get('ruoli_mantra')}</div>
                <span class="pill">MV {giocatore.get('media_voto')}</span>
                <span class="pill">FM {giocatore.get('fanta_media')}</span>
                <span class="pill pill-blue">Gol {giocatore.get('gol_fatti')}</span>
                <span class="pill pill-blue">Assist {giocatore.get('assist')}</span>
                <span class="pill pill-yellow">Q {giocatore.get('quotazione_attuale')}</span>
                <span class="pill pill-yellow">Q Mantra {giocatore.get('quotazione_attuale_mantra')}</span>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="price-panel">
                <div class="price-label">Prezzo corrente</div>
                <div class="price-number">{asta["prezzo_corrente"]}</div>
                <div class="price-credit">crediti</div>
                <div class="best-bidder">{nome_migliore}</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        prezzo_corrente = float(asta["prezzo_corrente"])
        minimo = prezzo_corrente + 1

        st.subheader("Rilancia")
        col_a, col_b, col_c, col_d, col_e = st.columns(5)

        with col_a:
            if st.button(f"+1 → {prezzo_corrente + 1}"):
                rilancia(asta, partecipante["id"], prezzo_corrente + 1)
                st.rerun()
        with col_b:
            if st.button(f"+5 → {prezzo_corrente + 5}"):
                rilancia(asta, partecipante["id"], prezzo_corrente + 5)
                st.rerun()
        with col_c:
            if st.button(f"+10 → {prezzo_corrente + 10}"):
                rilancia(asta, partecipante["id"], prezzo_corrente + 10)
                st.rerun()
        with col_d:
            if st.button(f"+20 → {prezzo_corrente + 20}"):
                rilancia(asta, partecipante["id"], prezzo_corrente + 20)
                st.rerun()
        with col_e:
            if st.button(f"+50 → {prezzo_corrente + 50}"):
                rilancia(asta, partecipante["id"], prezzo_corrente + 50)
                st.rerun()

        col_m1, col_m2 = st.columns([2, 1])
        with col_m1:
            offerta_custom = st.number_input("Offerta manuale", min_value=float(minimo), step=1.0)
        with col_m2:
            if st.button("Rilancia manualmente"):
                rilancia(asta, partecipante["id"], offerta_custom)
                st.rerun()

        st.divider()

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

        st.divider()

        st.subheader("Controlli banditore")
        c1, c2 = st.columns(2)

        with c1:
            if st.button("✅ Assegna al miglior offerente", type="primary"):
                assegna_giocatore(asta)
                st.rerun()

        with c2:
            if st.button("❌ Annulla asta"):
                annulla_asta(asta)
                st.rerun()

# =========================
# CHIAMA GIOCATORE
# =========================
elif pagina == "Chiama giocatore":
    st.header("📣 Chiama un giocatore")

    asta = get_asta_attiva(lega["id"])
    if asta:
        st.warning("C'è già un'asta attiva. Chiudila o annullala prima di chiamare un nuovo giocatore.")
    else:
        search = st.text_input("Cerca giocatore per nome")
        giocatori = get_giocatori(search, limit=100)

        if giocatori:
            df = pd.DataFrame(giocatori)

            colonne = [
                "id_giocatore", "nome", "squadra", "ruoli_mantra",
                "fanta_media", "quotazione_attuale", "quotazione_attuale_mantra"
            ]
            colonne = [c for c in colonne if c in df.columns]

            st.dataframe(df[colonne], use_container_width=True)

            options = [
                f"{g['id_giocatore']} - {g['nome']} | {g.get('squadra')} | {g.get('ruoli_mantra')}"
                for g in giocatori
            ]

            scelta = st.selectbox("Seleziona giocatore da chiamare", options)
            id_giocatore = int(scelta.split(" - ")[0])

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
# SCOUTING COMMENTI
# =========================
elif pagina == "Scouting / Commenti":
    st.header("🧠 Scouting / Commenti personali")

    st.markdown("""
    <div class="auction-grid-card">
        <div class="section-label">Database personale</div>
        Qui usi le statistiche storiche come base, ma aggiungi il tuo giudizio:
        fascia, priorità, prezzo massimo e commento personale.
    </div>
    """, unsafe_allow_html=True)

    search = st.text_input("Cerca giocatore da commentare")
    giocatori = get_giocatori(search, limit=100)

    if giocatori:
        options = [
            f"{g['id_giocatore']} - {g['nome']} | {g.get('squadra')} | {g.get('ruoli_mantra')}"
            for g in giocatori
        ]
        scelta = st.selectbox("Seleziona giocatore", options)
        id_giocatore = int(scelta.split(" - ")[0])
        giocatore = get_giocatore(id_giocatore)
        commento_old = get_commento_giocatore(lega["id"], id_giocatore)

        col1, col2 = st.columns([1.2, 1])

        with col1:
            st.markdown(f"""
            <div class="auction-grid-card">
                <div class="player-name-big">{giocatore.get('nome')}</div>
                <div class="player-meta">🏟️ {giocatore.get('squadra')} · 🎯 {giocatore.get('ruoli_mantra')}</div>
                <span class="pill">FM {giocatore.get('fanta_media')}</span>
                <span class="pill">MV {giocatore.get('media_voto')}</span>
                <span class="pill pill-blue">Gol {giocatore.get('gol_fatti')}</span>
                <span class="pill pill-blue">Assist {giocatore.get('assist')}</span>
                <span class="pill pill-yellow">Q {giocatore.get('quotazione_attuale')}</span>
                <span class="pill pill-yellow">Q Mantra {giocatore.get('quotazione_attuale_mantra')}</span>
            </div>
            """, unsafe_allow_html=True)

            dati_visibili = {
                "Partite a voto": giocatore.get("partite_a_voto"),
                "Media voto": giocatore.get("media_voto"),
                "Fanta media": giocatore.get("fanta_media"),
                "Gol fatti": giocatore.get("gol_fatti"),
                "Gol subiti": giocatore.get("gol_subiti"),
                "Rigori parati": giocatore.get("rigori_parati"),
                "Rigori calciati": giocatore.get("rigori_calciati"),
                "Rigori segnati": giocatore.get("rigori_segnati"),
                "Rigori sbagliati": giocatore.get("rigori_sbagliati"),
                "Assist": giocatore.get("assist"),
                "Ammonizioni": giocatore.get("ammonizioni"),
                "Espulsioni": giocatore.get("espulsioni"),
                "Autogol": giocatore.get("autogol"),
            }

            st.dataframe(pd.DataFrame([dati_visibili]).T.rename(columns={0: "Valore"}), use_container_width=True)

        with col2:
            st.subheader("Il tuo giudizio")

            fascia_default = commento_old.get("fascia") if commento_old else "Da valutare"
            priorita_default = commento_old.get("priorita") if commento_old else "Media"

            fasce = ["Top", "Semi-top", "Titolare utile", "Scommessa", "Riserva", "Da evitare", "Da valutare"]
            priorita_opzioni = ["Altissima", "Alta", "Media", "Bassa", "No"]

            fascia = st.selectbox(
                "Fascia",
                fasce,
                index=fasce.index(fascia_default) if fascia_default in fasce else fasce.index("Da valutare")
            )

            priorita = st.selectbox(
                "Priorità acquisto",
                priorita_opzioni,
                index=priorita_opzioni.index(priorita_default) if priorita_default in priorita_opzioni else priorita_opzioni.index("Media")
            )

            prezzo_massimo = st.number_input(
                "Prezzo massimo che pagheresti",
                min_value=0.0,
                value=float(commento_old.get("prezzo_massimo") or 0) if commento_old else 0.0,
                step=1.0
            )

            voto_personale = st.number_input(
                "Voto personale scouting",
                min_value=0.0,
                max_value=10.0,
                value=float(commento_old.get("voto_personale") or 6) if commento_old else 6.0,
                step=0.5
            )

            commento = st.text_area(
                "Commento personale",
                value=commento_old.get("commento") if commento_old else "",
                height=180,
                placeholder="Esempio: titolare, buoni bonus, da prendere solo se resta sotto i 20 crediti..."
            )

            if st.button("💾 Salva commento", type="primary"):
                salva_commento_giocatore(
                    lega["id"],
                    id_giocatore,
                    commento,
                    fascia,
                    priorita,
                    prezzo_massimo,
                    voto_personale
                )
                st.success("Commento salvato.")
                st.rerun()

    st.divider()
    st.subheader("📒 Tutti i commenti salvati")

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
        df_commenti = pd.DataFrame(rows)
        st.dataframe(df_commenti, use_container_width=True)
    else:
        st.info("Ancora nessun commento salvato.")

# =========================
# PARTECIPANTI
# =========================
elif pagina == "Partecipanti":
    st.header("👥 Partecipanti e crediti")
    partecipanti = get_partecipanti(lega["id"])
    st.dataframe(pd.DataFrame(partecipanti), use_container_width=True)

# =========================
# ROSE
# =========================
elif pagina == "Rose":
    st.header("🌹 Rose")

    rosa = get_rosa(lega["id"])
    partecipanti = get_partecipanti(lega["id"])

    if not rosa:
        st.info("Ancora nessun giocatore acquistato.")
    else:
        df_rosa = pd.DataFrame(rosa)

        for p in partecipanti:
            st.subheader(f"{p['nome_squadra']} - crediti: {p['crediti_residui']}")
            sub = df_rosa[df_rosa["partecipante_id"] == p["id"]]
            if sub.empty:
                st.caption("Nessun acquisto.")
            else:
                cols = ["nome_giocatore", "squadra_reale", "ruoli_mantra", "prezzo_acquisto"]
                st.dataframe(sub[cols], use_container_width=True)

# =========================
# DATABASE GIOCATORI
# =========================
elif pagina == "Database giocatori":
    st.header("📋 Database giocatori")

    search = st.text_input("Cerca nome")
    giocatori = get_giocatori(search, limit=300)

    if giocatori:
        df = pd.DataFrame(giocatori)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nessun giocatore trovato.")

# =========================
# ADMIN RESET
# =========================
elif pagina == "Admin / Reset":
    st.header("🧨 Admin / Reset prove")

    st.markdown("""
    <div class="danger-box">
        <b>Attenzione:</b> questa pagina serve per azzerare le prove dell'asta.
        Il reset cancella rose, rilanci, aste attive e riporta i crediti dei partecipanti al budget scelto.
        Il database dei giocatori NON viene cancellato.
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)
    with col1:
        budget_reset = st.number_input("Budget a cui riportare tutti", min_value=1.0, value=600.0, step=1.0)
    with col2:
        st.metric("Partecipanti", len(get_partecipanti(lega["id"])))
    with col3:
        st.metric("Lega", lega["codice_invito"])

    conferma = st.text_input("Per confermare scrivi RESET in maiuscolo")

    if conferma == "RESET":
        st.warning("Reset abilitato. Premi il pulsante qui sotto solo se sei sicuro.")
        if st.button("🧨 RESETTA TUTTA L'ASTA", type="primary"):
            reset_lega_totale(lega["id"], budget_reset)
            st.success("Reset completato: rose, rilanci e aste cancellati. Crediti ripristinati.")
            st.rerun()
    else:
        st.info("Scrivi RESET per sbloccare il pulsante di reset.")

    st.divider()
    st.subheader("Controllo rapido dati")

    c1, c2, c3 = st.columns(3)
    with c1:
        rose_count = len(get_rosa(lega["id"]))
        st.metric("Giocatori assegnati", rose_count)
    with c2:
        asta_attiva = get_asta_attiva(lega["id"])
        st.metric("Asta attiva", "Sì" if asta_attiva else "No")
    with c3:
        partecipanti_now = get_partecipanti(lega["id"])
        crediti_tot = sum(float(p["crediti_residui"]) for p in partecipanti_now)
        st.metric("Crediti totali residui", int(crediti_tot))
