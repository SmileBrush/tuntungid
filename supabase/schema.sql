-- Menggantikan tabel versi lama (client_briefs, projects). Data contoh lama ikut terhapus.
drop table if exists public.client_briefs cascade;
drop table if exists public.requests cascade;
drop table if exists public.project_files cascade;
drop table if exists public.projects cascade;
drop table if exists public.profiles cascade;

create table public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  full_name text not null,
  company text not null default '',
  created_at timestamptz not null default now()
);

create table public.projects (
  id uuid primary key default gen_random_uuid(),
  title text not null check (char_length(title) >= 3),
  stage integer not null default 1 check (stage between 1 and 5),
  start_date date,
  target_date date,
  client_id uuid not null references public.profiles (id) on delete cascade,
  created_at timestamptz not null default now()
);

create table public.project_files (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects (id) on delete cascade,
  label text not null,
  url text not null,
  created_at timestamptz not null default now()
);

create table public.requests (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects (id) on delete cascade,
  kind text not null check (kind in ('revisi', 'fitur_tambahan')),
  message text not null check (char_length(message) >= 5),
  status text not null default 'baru' check (status in ('baru', 'diproses', 'selesai')),
  admin_reply text,
  created_at timestamptz not null default now()
);

create index projects_client_id_idx on public.projects (client_id);
create index project_files_project_id_idx on public.project_files (project_id);
create index requests_project_id_idx on public.requests (project_id);

revoke all on public.profiles, public.projects, public.project_files, public.requests from anon;
grant usage on schema public to authenticated;
grant select, insert, update, delete on public.profiles, public.projects, public.project_files, public.requests to authenticated;

alter table public.profiles enable row level security;
alter table public.projects enable row level security;
alter table public.project_files enable row level security;
alter table public.requests enable row level security;

-- Peran admin dibaca dari app_metadata (tidak bisa diubah pengguna sendiri).
create policy "admin penuh profiles" on public.profiles for all to authenticated
  using (((select auth.jwt()) -> 'app_metadata' ->> 'role') = 'admin')
  with check (((select auth.jwt()) -> 'app_metadata' ->> 'role') = 'admin');
create policy "klien baca profil sendiri" on public.profiles for select to authenticated
  using ((select auth.uid()) = id);

create policy "admin penuh projects" on public.projects for all to authenticated
  using (((select auth.jwt()) -> 'app_metadata' ->> 'role') = 'admin')
  with check (((select auth.jwt()) -> 'app_metadata' ->> 'role') = 'admin');
create policy "klien baca proyek sendiri" on public.projects for select to authenticated
  using ((select auth.uid()) = client_id);

create policy "admin penuh project_files" on public.project_files for all to authenticated
  using (((select auth.jwt()) -> 'app_metadata' ->> 'role') = 'admin')
  with check (((select auth.jwt()) -> 'app_metadata' ->> 'role') = 'admin');
create policy "klien baca file proyek sendiri" on public.project_files for select to authenticated
  using (exists (
    select 1 from public.projects p
    where p.id = project_files.project_id and p.client_id = (select auth.uid())
  ));

create policy "admin penuh requests" on public.requests for all to authenticated
  using (((select auth.jwt()) -> 'app_metadata' ->> 'role') = 'admin')
  with check (((select auth.jwt()) -> 'app_metadata' ->> 'role') = 'admin');
create policy "klien baca permintaan sendiri" on public.requests for select to authenticated
  using (exists (
    select 1 from public.projects p
    where p.id = requests.project_id and p.client_id = (select auth.uid())
  ));
create policy "klien kirim permintaan proyek sendiri" on public.requests for insert to authenticated
  with check (
    status = 'baru' and admin_reply is null and exists (
      select 1 from public.projects p
      where p.id = requests.project_id and p.client_id = (select auth.uid())
    )
  );

notify pgrst, 'reload schema';
