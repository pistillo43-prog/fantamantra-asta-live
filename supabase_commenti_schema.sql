
create table if not exists commenti_giocatori (
  id uuid primary key default gen_random_uuid(),
  lega_id uuid references leghe(id) on delete cascade,
  id_giocatore integer references giocatori(id_giocatore) on delete cascade,
  commento text,
  fascia text,
  priorita text,
  prezzo_massimo numeric,
  voto_personale numeric,
  created_at timestamp default now(),
  updated_at timestamp default now(),
  unique (lega_id, id_giocatore)
);
