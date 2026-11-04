-- Jalankan skrip ini di SQL Editor Supabase untuk menambahkan fitur Portofolio dan Review Klien.

-- 1. Tabel Portofolio
create table if not exists public.portfolios (
  id uuid primary key default gen_random_uuid(),
  title text not null check (char_length(title) >= 3),
  sector text not null default 'Aplikasi Web',
  summary text not null check (char_length(summary) >= 5),
  tech_stack text not null default 'Next.js + Supabase',
  image_url text not null,
  demo_url text,
  is_published boolean not null default true,
  created_at timestamptz not null default now()
);

-- 2. Tabel Review Klien
create table if not exists public.reviews (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects (id) on delete cascade,
  client_id uuid not null references public.profiles (id) on delete cascade,
  rating integer not null check (rating between 1 and 5),
  feedback text not null check (char_length(feedback) >= 5),
  is_published boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint unique_project_review unique (project_id)
);

create index if not exists portfolios_published_idx on public.portfolios (is_published);
create index if not exists reviews_published_idx on public.reviews (is_published);
create index if not exists reviews_client_id_idx on public.reviews (client_id);
create index if not exists reviews_project_id_idx on public.reviews (project_id);

grant usage on schema public to anon, authenticated;
grant select on public.portfolios to anon;
grant select on public.reviews to anon;
grant select, insert, update, delete on public.portfolios to authenticated;
grant select, insert, update, delete on public.reviews to authenticated;

alter table public.portfolios enable row level security;
alter table public.reviews enable row level security;

-- Kebijakan Portofolio:
-- Publik dapat melihat portofolio yang disetujui (is_published = true)
drop policy if exists "publik baca portofolio rilis" on public.portfolios;
create policy "publik baca portofolio rilis" on public.portfolios for select to anon, authenticated
  using (is_published = true);

-- Admin memiliki akses penuh ke seluruh portofolio
drop policy if exists "admin penuh portfolios" on public.portfolios;
create policy "admin penuh portfolios" on public.portfolios for all to authenticated
  using (((select auth.jwt()) -> 'app_metadata' ->> 'role') = 'admin')
  with check (((select auth.jwt()) -> 'app_metadata' ->> 'role') = 'admin');

-- Kebijakan Review:
-- Publik dapat melihat review yang telah disetujui Admin (is_published = true)
drop policy if exists "publik baca review rilis" on public.reviews;
create policy "publik baca review rilis" on public.reviews for select to anon, authenticated
  using (is_published = true);

-- Klien dapat membaca review miliknya sendiri
drop policy if exists "klien baca review sendiri" on public.reviews;
create policy "klien baca review sendiri" on public.reviews for select to authenticated
  using ((select auth.uid()) = client_id);

-- Klien dapat mengisi/mengubah review hanya jika proyeknya miliknya dan sudah masuk Tahap 5
drop policy if exists "klien isi review tahap 5" on public.reviews;
create policy "klien isi review tahap 5" on public.reviews for insert to authenticated
  with check (
    (select auth.uid()) = client_id and
    is_published = false and
    exists (
      select 1 from public.projects p
      where p.id = reviews.project_id and p.client_id = (select auth.uid()) and p.stage = 5
    )
  );

drop policy if exists "klien perbarui review tahap 5" on public.reviews;
create policy "klien perbarui review tahap 5" on public.reviews for update to authenticated
  using (
    (select auth.uid()) = client_id and
    exists (
      select 1 from public.projects p
      where p.id = reviews.project_id and p.client_id = (select auth.uid()) and p.stage = 5
    )
  )
  with check (
    (select auth.uid()) = client_id and
    is_published = false
  );

-- Admin memiliki akses penuh ke seluruh review (menyetujui publikasi, menghapus, dll)
drop policy if exists "admin penuh reviews" on public.reviews;
create policy "admin penuh reviews" on public.reviews for all to authenticated
  using (((select auth.jwt()) -> 'app_metadata' ->> 'role') = 'admin')
  with check (((select auth.jwt()) -> 'app_metadata' ->> 'role') = 'admin');

notify pgrst, 'reload schema';
