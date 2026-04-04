-- À exécuter dans Supabase : SQL Editor → New query → Run
-- Table pour l’historique des tentatives de connexion au guide (codes-acces.html)

create table if not exists public.guide_access_attempts (
  id uuid default gen_random_uuid() primary key,
  code_text text not null,
  outcome text not null check (outcome in ('ok', 'fail')),
  reason text,
  created_at timestamptz default now() not null
);

comment on table public.guide_access_attempts is
  'Tentatives de saisie du code sur codes-acces.html (site statique).';

create index if not exists guide_access_attempts_created_at_idx
  on public.guide_access_attempts (created_at desc);

alter table public.guide_access_attempts enable row level security;

drop policy if exists "Allow anon insert guide access log" on public.guide_access_attempts;
drop policy if exists "Allow insert guide access log" on public.guide_access_attempts;

-- Insertion depuis le navigateur (clé publiable / anon) — politique large pour tous les rôles clients
create policy "Allow insert guide access log"
on public.guide_access_attempts for insert
with check (true);

-- Lecture : tableau Supabase ou admin avec la clé secrète uniquement (service_role contourne RLS)

grant insert on public.guide_access_attempts to anon;
grant insert on public.guide_access_attempts to authenticated;
grant usage on schema public to anon;
grant usage on schema public to authenticated;
