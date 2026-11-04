# Spesifikasi Desain: Fitur Portofolio dan Review Klien

Tanggal: 2026-11-04
Jalur: Architectural
Topik: Subsistem Portofolio Dinamis dan Review Klien Terverifikasi

## 1. Ringkasan & Tujuan
Menambahkan dua kemampuan baru pada ekosistem Tuntung.id:
1. **Portofolio Proyek**: Dikelola oleh Admin di Dashboard Admin, ditampilkan ke publik di Landing Page untuk membuktikan hasil kerja nyata 2 programmer.
2. **Review Klien**: Ditulis langsung oleh klien di Dashboard Klien khusus saat proyek mencapai Tahap 5 (Serah Terima & Garansi), dimoderasi oleh Admin (toggle persetujuan publik), dan ditampilkan di Landing Page secara jujur (mematuhi standar antislop R-18 tanpa data fiktif).

---

## 2. Struktur Database PostgreSQL (Supabase)

### A. Tabel `public.portfolios`
Tabel untuk menyimpan portofolio hasil kerja yang diinput oleh Admin:
- `id` (UUID, Primary Key, default `gen_random_uuid()`)
- `title` (Text, Nama proyek aplikasi, minimal 3 karakter)
- `sector` (Text, Sektor bisnis klien, misal "UMKM & Ritel", "Kesehatan", "Pendidikan")
- `summary` (Text, Ringkasan solusi operasional yang dibangun, 1-2 kalimat)
- `tech_stack` (Text, Stack teknologi yang digunakan, misal "Next.js + Supabase")
- `image_url` (Text, Tautan URL gambar tangkapan layar / preview mockup)
- `demo_url` (Text, Tautan situs live atau demo proyek, opsional)
- `is_published` (Boolean, default `true`, pengatur tampil di landing page)
- `created_at` (Timestamptz, default `now()`)

### B. Tabel `public.reviews`
Tabel untuk menyimpan penilaian dan testimoni otentik klien:
- `id` (UUID, Primary Key, default `gen_random_uuid()`)
- `project_id` (UUID, Foreign Key ke `public.projects(id)` on delete cascade)
- `client_id` (UUID, Foreign Key ke `public.profiles(id)` on delete cascade)
- `rating` (Integer, nilai 1 sampai 5)
- `feedback` (Text, ulasan jujur klien, minimal 5 karakter)
- `is_published` (Boolean, default `false`, hanya tampil di publik jika disetujui Admin)
- `created_at` (Timestamptz, default `now()`)
- `updated_at` (Timestamptz, default `now()`)

Constraint unik: `UNIQUE(project_id)` agar setiap proyek hanya memiliki satu ulasan resmi yang dapat diperbarui oleh klien.

### C. Kebijakan Keamanan (Row Level Security)
1. **Hak Akses Publik (`anon`)**:
   - `SELECT` pada `public.portfolios` hanya untuk baris dengan `is_published = true`.
   - `SELECT` pada `public.reviews` hanya untuk baris dengan `is_published = true`.
2. **Hak Akses Klien (`authenticated`)**:
   - `SELECT` pada `public.reviews` miliknya sendiri (`client_id = auth.uid()`).
   - `INSERT` dan `UPDATE` pada `public.reviews` hanya diizinkan jika klien adalah pemilik proyek (`projects.client_id = auth.uid()`) dan proyek tersebut berstatus Tahap 5 (`projects.stage = 5`).
3. **Hak Akses Admin (`authenticated` dengan peran admin)**:
   - Akses penuh (`ALL`: `SELECT`, `INSERT`, `UPDATE`, `DELETE`) pada kedua tabel berdasarkan verifikasi `(((select auth.jwt()) -> 'app_metadata' ->> 'role') = 'admin')`.

---

## 3. Alur Pengguna & Antarmuka

### A. Dashboard Klien (`/klien`)
1. **Kondisi Proyek di Tahap 5**:
   - Muncul kartu baru "Beri Penilaian & Review Proyek".
   - Terdapat pilihan rating bintang 1 sampai 5 dan textarea untuk ulasan.
   - Jika sudah pernah mengirim, form menampilkan isi ulasan sebelumnya dengan tombol "Perbarui Review".
   - Terdapat penanda status: "Ulasan Anda telah tersimpan dan menunggu peninjauan admin untuk ditampilkan di beranda".
2. **Kondisi Proyek di Tahap 1 sampai 4**:
   - Kartu ulasan menampilkan pesan edukatif yang ramah: "Formulir ulasan akan aktif secara otomatis saat proyek Anda memasuki Tahap 5 (Serah Terima & Garansi)".

### B. Dashboard Admin (`/admin`)
1. **Tab Portofolio**:
   - Form pembuatan portofolio baru (Judul, Sektor, Ringkasan Solusi, Tech Stack, URL Gambar, URL Demo).
   - Daftar portofolio yang ada dengan tombol aksi: Toggle Publikasi (Tampilkan / Sembunyikan) dan Hapus Portofolio.
2. **Tab Review**:
   - Menampilkan seluruh review yang masuk dari klien.
   - Menampilkan detail: Nama Klien, Nama Proyek, Bintang Rating, Tanggal, dan Pesan Ulasan.
   - Tombol toggle status: "Setujui & Tampilkan di Landing Page" atau "Sembunyikan dari Publik".

### C. Landing Page Publik (`/`)
1. **Bagian Portofolio**:
   - Ditempatkan setelah bagian Layanan dan Metode Kerja.
   - Kartu portofolio menampilkan gambar tangkapan layar, tag sektor, judul aplikasi, ringkasan manfaat, tag teknologi, dan tombol "Lihat Demo" (jika tersedia).
2. **Bagian Review Klien**:
   - Ditempatkan sebelum bagian CTA Kontak / Penutup.
   - Menampilkan kutipan ulasan klien asli, bintang warna emas (`#F4B41A`), nama klien, dan nama instansi/perusahaan.
   - Memenuhi kaidah tanpa testimoni fiktif: jika belum ada ulasan yang disetujui, bagian ini tidak akan memuat nama rekaan.

---

## 4. Rencana Pengujian & Verifikasi
1. **Unit Test**: Uji validasi input rating (1-5), batas karakter review, dan pengecekan hak akses tahap 5.
2. **Uji RLS Supabase**:
   - Memastikan pengguna anonim tidak bisa membaca review yang `is_published = false`.
   - Memastikan klien pada proyek tahap 1-4 ditolak oleh RLS saat mencoba insert review.
3. **Uji Antarmuka Nyata**:
   - Admin menambah portofolio baru -> langsung muncul di Landing Page.
   - Admin mengubah status proyek klien ke tahap 5 -> form ulasan aktif di dashboard klien.
   - Klien mengirim review -> muncul di dashboard admin -> admin klik setujui -> muncul di Landing Page.
