# Tuntung.id: Rombak Total (Landing, Dashboard Klien, Dashboard Admin)

Tanggal: 2026-11-04
Jalur: Architectural
Menggantikan: `2026-11-04-tuntungid-ui-and-workflow-design.md`

## Tujuan

Aplikasi bisnis jasa pembuatan aplikasi dan web app milik 2 programmer Tuntung.id. Tiga permukaan: landing page publik, Dashboard Klien, Dashboard Admin. Teks seminimal mungkin, tampilan profesional.

## Keputusan yang sudah disetujui

| Topik | Keputusan |
|---|---|
| Fungsi Dashboard Klien | Pantau progres tahap 1 sampai 5, jadwal, file serah terima, kirim permintaan revisi atau fitur tambahan |
| Akun klien | Dibuat admin dari Dashboard Admin, klien tidak bisa mendaftar sendiri |
| Akun admin | Dibuat manual di Supabase (Authentication > Users), peran disimpan di `app_metadata.role = "admin"` |
| Hosting | Vercel (gratis) |
| Database dan Auth | Supabase gratis (PostgreSQL, Auth, RLS) |
| Warna | Struktur ChronoTask dengan warna merek Tuntung.id |
| Bagian Tim di landing | Dihapus |

## Pendekatan

Next.js 15 (App Router) dengan Supabase Auth lewat `@supabase/ssr`, RLS aktif di semua tabel. Akun klien dibuat lewat aksi server dengan secret key yang hanya ada di env Vercel dan tidak pernah memakai prefiks `NEXT_PUBLIC_`.

Dihapus: simulator beban manual, wizard 6 langkah, penyimpanan localStorage, kalkulator add-on, panel input URL dan key Supabase di browser.

## Rute

| Rute | Akses | Isi |
|---|---|---|
| `/` | Publik | Landing ringkas |
| `/masuk` | Publik | Form email dan kata sandi, pengalihan sesuai peran |
| `/klien` | Klien | Progres, jadwal, file serah terima, permintaan |
| `/admin` | Admin | Proyek, klien, ubah tahap, balas permintaan, buat akun klien |

Perlindungan rute dilakukan di server (middleware dan pengecekan sesi di layout). Klien yang membuka `/admin` dialihkan ke `/klien`. Pengguna tanpa sesi dialihkan ke `/masuk`.

## Landing page

Satu judul dan satu kalimat pendek per bagian.
1. Hero: "Gawi Manuntung, Supaya Untung", satu kalimat, satu tombol "Jadwalkan Audit Gratis" (membuka WhatsApp dengan pesan terisi), kartu UI mengambang.
2. Layanan: 3 kartu (Audit Gratis 30 Menit, Aplikasi Kustom dan Otomasi, Pendampingan dan Garansi 30 Hari).
3. Metode Kerja: 5 tahap dalam satu baris.
4. Dashboard: cuplikan Dashboard Klien.
5. Kontak: tombol WhatsApp dan footer.

Nomor WhatsApp berupa placeholder `[REAL DATA]` yang diisi pemilik lewat env `NEXT_PUBLIC_WHATSAPP_NUMBER`. Tidak ada testimoni, statistik, atau nama klien karangan.

## Data (Supabase, semua tabel RLS aktif)

- `profiles`: `id` (FK `auth.users`), `full_name`, `company`.
- `projects`: `id`, `title`, `stage` (1 sampai 5), `start_date`, `target_date`, `client_id` (FK `profiles`), `created_at`.
- `project_files`: `id`, `project_id`, `label`, `url`, `created_at`.
- `requests`: `id`, `project_id`, `kind` (revisi atau fitur_tambahan), `message`, `status` (baru, diproses, selesai), `admin_reply`, `created_at`.

Kebijakan akses:
- Klien: `SELECT` pada proyek miliknya (`client_id = auth.uid()`), file proyek miliknya, dan permintaannya. `INSERT` pada `requests` hanya untuk proyek miliknya.
- Admin (`auth.jwt() -> app_metadata ->> 'role' = 'admin'`): akses penuh ke semua tabel.
- Tidak ada kebijakan berbasis `user_metadata`.
- Tidak ada `SECURITY DEFINER` di schema `public`.

## Tampilan

- Latar abu terang bertekstur titik halus, kartu putih dengan bayangan lembut, tombol utama hijau `#187941` sebagai satu-satunya aksen aksi, kuning hanya untuk satu penanda kecil.
- Font: Montserrat (judul) dan Inter (isi).
- Dashboard: sidebar ringan dan kartu putih, mengikuti pola ChronoTask.
- Setiap tampilan data punya kondisi kosong (dengan tombol aksi), memuat (dengan teks konteks), dan gagal (dengan penjelasan dan cara mengatasi).
- Responsif: mobile menyusun ulang tata letak, bukan sekadar mengecil. Target sentuh minimal 44x44px.
- Kepatuhan: `AGENTS.md` dan `antislop` (tanpa em-dash, tanpa data karangan, CTA spesifik).

## Struktur kode

- `src/lib/supabase/`: pembuat client server dan browser (Interface kecil, satu tempat konfigurasi).
- `src/lib/access.js`: satu fungsi `resolveRole(user)` yang mengembalikan `admin`, `client`, atau `anonymous`, dipakai middleware dan layout.
- `src/app/(public)`, `src/app/masuk`, `src/app/klien`, `src/app/admin`.
- `supabase/schema.sql`: tabel, grant, RLS, dan policy.
- `tests/`: uji `resolveRole` dan aturan transisi tahap.

## Verifikasi

- `npm test` lulus.
- Build dan server lokal tanpa error konsol.
- Klik nyata di browser: login klien, login admin, pengalihan peran, buat akun klien, ubah tahap, kirim dan balas permintaan.
- Uji akses: klien tidak bisa membaca proyek klien lain.
- `lint.mjs`, `inspect.mjs`, dan Delivery Gate `antislop` dijalankan di akhir.

## Di luar cakupan

Tagihan dan pembayaran, unggah file langsung (file serah terima berupa tautan), notifikasi email otomatis, pendaftaran mandiri klien.

