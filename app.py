
import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, timedelta

st.set_page_config(
    page_title="FantaMantra Asta Live",
    page_icon="⚽",
    layout="wide"
)


st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #111827 45%, #1e293b 100%);
        color: #f8fafc;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617 0%, #111827 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 800 !important;
    }

    .stMarkdown, .stText, p, label, span {
        color: #e5e7eb;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.08);
        padding: 18px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    }

    div[data-testid="stMetric"] label {
        color: #cbd5e1 !important;
    }

    div[data-testid="stMetric"] div {
        color: #ffffff !important;
    }

    .fantacard {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 22px;
        padding: 22px;
        margin: 12px 0;
        box-shadow: 0 14px 35px rgba(0,0,0,0.28);
    }

    .big-player {
        font-size: 42px;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .pill {
        display: inline-block;
        background: rgba(59,130,246,0.18);
        color: #bfdbfe;
        padding: 7px 12px;
        border-radius: 999px;
        margin-right: 8px;
        margin-top: 8px;
        border: 1px solid rgba(96,165,250,0.35);
        font-weight: 700;
    }

    .price-box {
        background: linear-gradient(135deg, #f59e0b, #ef4444);
        border-radius: 24px;
        padding: 24px;
        text-align: center;
        color: white;
        box-shadow: 0 16px 40px rgba(239,68,68,0.25);
    }

    .price-number {
        font-size: 56px;
        font-weight: 900;
        line-height: 1;
    }

    .price-label {
        font-size: 16px;
        opacity: 0.9;
        font-weight: 700;
    }

    .danger-box {
        background: rgba(239,68,68,0.15);
        border: 1px solid rgba(239,68,68,0.45);
        border-radius: 18px;
        padding: 18px;
    }

    .success-box {
        background: rgba(34,197,94,0.14);
        border: 1px solid rgba(34,197,94,0.35);
        border-radius: 18px;
        padding: 18px;
    }

    button[kind="primary"] {
        border-radius: 14px !important;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# CONFIG SUPABASE
# =========================
# In locale puoi inserirli nella sidebar.
# Su Streamlit Cloud li metteremo nei Secrets.
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
    """
    Reset completo della lega per fare prove:
    - elimina rose
    - elimina rilanci
    - elimina aste live
    - riporta crediti partecipanti al budget scelto
    """
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
<div class="fantacard">
    <div style="font-size:54px;font-weight:900;">⚽ FantaMantra Asta Live</div>
    <div style="font-size:18px;color:#cbd5e1;margin-top:6px;">
        Sala d'asta Mantra collegata a Supabase: crediti, rose e rilanci sempre aggiornati.
    </div>
</div>
""", unsafe_allow_html=True)

if st.session_state.lega is None:
    st.subheader("Entra nella lega")

    codice = st.text_input("Codice invito lega", value="FANTA26").upper().strip()

    if st.button("Entra"):
        lega = get_lega_by_codice(codice)
        if lega:
            st.session_state.lega = lega
            st.rerun()
        else:
            st.error("Codice lega non trovato.")

    st.stop()


lega = st.session_state.lega

st.sidebar.success(f"Lega: {lega['nome']}")
st.sidebar.write(f"Codice: `{lega['codice_invito']}`")


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
# PAGINE
# =========================
pagina = st.sidebar.radio(
    "Menu",
    ["Sala asta", "Chiama giocatore", "Scouting / Commenti", "Partecipanti", "Rose", "Database giocatori", "Admin / Reset"]
)

# refresh manuale
if st.sidebar.button("Aggiorna"):
    st.rerun()


# =========================
# SALA ASTA
# =========================
if pagina == "Sala asta":
    st.header("🔥 Sala asta live")

    asta = get_asta_attiva(lega["id"])

    if not asta:
        st.info("Nessun giocatore attualmente all'asta.")
    else:
        giocatore = get_giocatore(asta["id_giocatore"])

        col1, col2 = st.columns([2, 1])

        nome_migliore = "Nessuna offerta"
        if asta.get("partecipante_corrente"):
            migliore = [p for p in partecipanti if p["id"] == asta["partecipante_corrente"]]
            if migliore:
                nome_migliore = migliore[0]["nome_squadra"]

        with col1:
            st.markdown(f"""
            <div class="fantacard">
                <div class="big-player">{giocatore.get('nome')}</div>
                <span class="pill">🏟️ {giocatore.get('squadra')}</span>
                <span class="pill">🎯 {giocatore.get('ruoli_mantra')}</span>
                <span class="pill">⭐ Fanta media: {giocatore.get('fanta_media')}</span>
                <span class="pill">💰 Q: {giocatore.get('quotazione_attuale')}</span>
                <span class="pill">🧩 Q Mantra: {giocatore.get('quotazione_attuale_mantra')}</span>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="price-box">
                <div class="price-label">PREZZO CORRENTE</div>
                <div class="price-number">{asta["prezzo_corrente"]}</div>
                <div style="margin-top:14px;font-weight:800;">Miglior offerente</div>
                <div>{nome_migliore}</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        prezzo_corrente = float(asta["prezzo_corrente"])
        minimo = prezzo_corrente + 1

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            if st.button(f"+1 → {prezzo_corrente + 1}"):
                rilancia(asta, partecipante["id"], prezzo_corrente + 1)
                st.rerun()

        with col_b:
            if st.button(f"+5 → {prezzo_corrente + 5}"):
                rilancia(asta, partecipante["id"], prezzo_corrente + 5)
                st.rerun()

        with col_c:
            offerta_custom = st.number_input("Offerta manuale", min_value=float(minimo), step=1.0)
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
        st.caption("Per ora tutti vedono questi pulsanti. Più avanti metteremo il ruolo admin.")

        c1, c2 = st.columns(2)

        with c1:
            if st.button("✅ Assegna al miglior offerente"):
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
                if st.button("🚀 Avvia asta"):
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
    <div class="fantacard">
        Qui usi le statistiche vecchie come base, ma aggiungi il tuo giudizio:
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
            <div class="fantacard">
                <div class="big-player">{giocatore.get('nome')}</div>
                <span class="pill">🏟️ {giocatore.get('squadra')}</span>
                <span class="pill">🎯 {giocatore.get('ruoli_mantra')}</span>
                <span class="pill">⭐ Fanta media: {giocatore.get('fanta_media')}</span>
                <span class="pill">📊 Media voto: {giocatore.get('media_voto')}</span>
                <span class="pill">⚽ Gol: {giocatore.get('gol_fatti')}</span>
                <span class="pill">🅰️ Assist: {giocatore.get('assist')}</span>
                <span class="pill">💰 Quotazione: {giocatore.get('quotazione_attuale')}</span>
                <span class="pill">🧩 Quotazione Mantra: {giocatore.get('quotazione_attuale_mantra')}</span>
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

            if st.button("💾 Salva commento"):
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
