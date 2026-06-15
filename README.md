
# FantaMantra Asta Live

App Streamlit collegata a Supabase per asta Fantacalcio Mantra live.

## Avvio locale

Dentro la cartella del progetto:

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

Poi nella sidebar inserisci:

- Supabase URL
- Supabase anon key

Li trovi in Supabase:

Project Settings → API

## Tabelle richieste

- leghe
- partecipanti
- giocatori
- rose
- offerte
- asta_live
- rilanci

## Nota

Per la prima versione tutti vedono i controlli da banditore.
Nella versione successiva aggiungeremo ruolo admin e permessi.


## Novità v2

- Pagina Admin / Reset
- Reset rose, rilanci e aste
- Ripristino crediti a 600
- Interfaccia più curata con card e stile dark


## Novità v3

- Pagina Scouting / Commenti
- Commenti personali per ogni giocatore
- Fascia, priorità, prezzo massimo e voto scouting
- Tabella Supabase `commenti_giocatori`
