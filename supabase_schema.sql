-- ARION Team OS Supabase Schema
-- Supabase SQL Editor에서 실행하세요.

create table if not exists public.arion_records (
  id bigserial primary key,
  table_key text not null,
  data jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists arion_records_table_key_idx
on public.arion_records (table_key);

alter table public.arion_records enable row level security;

-- 주의:
-- 이 MVP는 Streamlit 서버에서 service_role key로 접근합니다.
-- service_role key는 Streamlit Secrets에만 저장하고 GitHub에 절대 올리지 마세요.
-- 일반 anon 공개 정책은 만들지 않습니다.
