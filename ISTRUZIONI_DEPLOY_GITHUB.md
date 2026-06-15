
# Come caricare su GitHub in sicurezza

Questa versione NON contiene il file `.streamlit/secrets.toml`.

## 1. Apri il terminale in questa cartella

Devi essere nella cartella dove ci sono:

- app.py
- requirements.txt
- .gitignore
- README.md

## 2. Comandi Git

Sostituisci `TUO_USERNAME` con il tuo username GitHub.

```cmd
git init
git add .
git commit -m "Prima versione FantaMantra Asta Live"
git branch -M main
git remote add origin https://github.com/TUO_USERNAME/fantamantra-asta-live.git
git push -u origin main
```

## 3. Streamlit Cloud

Vai su Streamlit Cloud, crea una nuova app e scegli:

- Repository: fantamantra-asta-live
- Branch: main
- Main file path: app.py

## 4. Secrets su Streamlit Cloud

In Advanced settings -> Secrets inserisci:

```toml
SUPABASE_URL = "https://davmwirfdrsepwrkdkiq.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_ojOjLrItLA-5W4mhU8q61g_wgt3raZj"
```

Non mettere mai questi valori dentro GitHub.
