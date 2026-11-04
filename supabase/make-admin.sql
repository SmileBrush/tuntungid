-- Jalankan di SQL Editor Supabase. Ganti email sesuai akun admin yang sudah dibuat di Authentication > Users.
update auth.users
set raw_app_meta_data = coalesce(raw_app_meta_data, '{}'::jsonb) || '{"role": "admin"}'::jsonb
where email in ('rahman.andry.m@gmail.com');

-- Periksa hasilnya: kolom role harus berisi admin.
select email, raw_app_meta_data ->> 'role' as role from auth.users;

