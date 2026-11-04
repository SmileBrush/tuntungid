# Spesifikasi Arsitektur & Desain UI: Tuntung.id (Next.js + Tailwind CSS + Supabase + Cloudflare Pages)

- **Tanggal**: 4 November 2026
- **Jalur Brainstorming**: `Architectural`
- **Tim Pengembang**: *The Power Duo* (2 Programmer: *Solution Architect & Conceptor* + *Automation & App Engineer*)
- **Target Deployment Gratis**: **Cloudflare Pages** (Hosting Web Gratis, Bandwidth Unlimited, Bebas Komersial) + **Supabase PostgreSQL** / **Cloudflare D1** (Database Cloud Gratis).

---

## 1. Ringkasan Eksekutif & Posisi Produk

**Tuntung.id** (*"Gawi Manuntung, Supaya Untung"*) adalah bisnis pengembangan aplikasi web kustom, micro-app, integrasi API, dan otomasi operasional untuk UMKM, instansi pendidikan, fasilitas kesehatan, serta perkantoran. Berbeda dari agensi yang hanya terpaku pada satu platform, Tuntung.id membangun solusi lintas teknologi (Web App Full-Stack, Database SQL/Cloud, REST API, WhatsApp Gateway, PDF Otomatis, hingga Google Workspace sesuai kebutuhan klien).

Aplikasi web Tuntung.id ini terdiri atas dua permukaan (*surface*) yang saling terhubung:
1. **Landing Page Marketing (`/` - Mode `Persuade`)**:
   - Mengadaptasi komposisi **ChronoTask SaaS** yang telah disetujui di [tuntungid.figcraft](file:///d:/APLIKASI/Project%20Ane/tuntungid/tuntungid.figcraft):
     - **Centered Hero + 4 Floating Widgets**: Sticky Note kuning (*"Gawi Manuntung, Supaya Untung"*), Kartu Sesi Audit Gratis 30 Menit, Kartu Solusi Aplikasi Lintas Sektor, dan Kartu Teknologi & Integrasi Fleksibel (`Web App`, `SQL / API`, `Otomasi`).
     - **Live Interactive Workflow & Scope Estimator**: Pengunjung dapat memilih sektor usaha (*UMKM*, *Faskes*, *Pendidikan*, *Perkantoran*), memilih modul fitur yang dibutuhkan, dan langsung mengirimkannya ke formulir **6 Poin Client Brief**.
     - **Solutions + Embedded Dashboard Preview**: Pratinjau interaktif layar kerja *Tuntung Studio* berbingkai hijau (`#22A45D`) lengkap dengan checklist standar proyek, jaminan garansi 30 hari, grafik cincin kepatuhan (`6/6 Brief`, `5/5 T&C`, `5 Tahap Kerja`), dan bar progres 5 tahap.
     - **Bento Grid 2x2 ("Semua proses pembuatan aplikasi di satu tempat")**: Menampilkan peran *The Power Duo* (2 programmer), diagnosa 6 poin Client Brief, transparansi 5 poin T&C & mekanisme *Add-on*, serta cakupan lintas sektor.
     - **Tech & Platform Integrations Grid**: 7 ubin kapabilitas teknis (`Web App`, `SQL / DB`, `REST API`, `WhatsApp`, `Dokumen PDF`, `Cloud / VPS`, `Workspace`).
     - **3 Kartu Layanan Utama**: *Sesi Audit & Konsultasi Gratis (30 Menit)*, *Custom Micro-App & Otomasi* (Kartu Utama), dan *Onboarding & Maintenance (Garansi 30 Hari + Opsi Retainer)*.
     - **Footer dengan Floating Tiles**: Slogan *"Gawi Manuntung, Supaya Untung"*, navigasi lengkap tanpa panah dekoratif (`R-08`), dan 8 ubin alur kerja.
2. **Dashboard Workspace & Portal Klien (`/workspace` atau Tab Terpadu - Mode `Operate`)**:
   - Mengikuti desain halaman ke-2 dan ke-3 pada [tuntungid.figcraft](file:///d:/APLIKASI/Project%20Ane/tuntungid/tuntungid.figcraft):
     - **Tab 1: Workspace Kendali Proyek & The Power Duo**:
       - Sapaan ruang kerja, tombol peralihan peran (*Solution Architect & Conceptor* vs *Automation & App Engineer*), checklist standar proyek, kartu Garansi 30 Hari (`Lapor Bug Rp 0` vs `+ Hitung Add-on`), grafik cincin kepatuhan (`6/6 Poin Brief`, `5/5 Poin T&C`, `100% Data Milik Klien`), dan pelacak **5 Tahap Metode Kerja**.
       - Menyediakan penguji **Empty State**, **Loading State**, dan **Error State** sesuai standar aksesibilitas manusia (`R-27`).
     - **Tab 2: Formulir Interaktif 6 Poin Client Brief & Booking Audit 30 Menit**:
       - Formulir 6 langkah sesuai brief (*1. Profil & Identitas Bisnis, 2. Problem & QoL Goal, 3. Alur Kerja Saat Ini, 4. Spesifikasi & Fitur, 5. Data & Bahan Awal, 6. Timeline, Anggaran & Jadwal Audit 30 Menit*).
     - **Tab 3: Persetujuan Digital 5 Poin Terms & Conditions (T&C) & Scope Guard**:
       - Checklist persetujuan 5 poin T&C untuk mengunci *Scope Baseline* sebelum proyek dapat berpindah dari Tahap 2 (*Perancangan Prototype MVP*) ke Tahap 3 (*Eksekusi & Development*).
       - Dilengkapi kalkulator transparan untuk membedakan **Perbaikan Bug Masa Garansi 30 Hari (`Rp 0`)** dengan **Penambahan Fitur Baru (`Add-on`)**.

---

## 2. Arsitektur Deep Modules (`codebase-design`)

Seluruh logika bisnis ditempatkan pada modul murni yang terpisah dari komponen React agar mudah diuji (*unit test*) dan bebas dari kebocoran efek samping:

| Nama Modul | File | Interface Utama | Tanggung Jawab Deep Implementation |
| :--- | :--- | :--- | :--- |
| **`WorkspaceStorageAdapter`** | [`src/modules/storage-adapter.js`](file:///d:/APLIKASI/Project%20Ane/tuntungid/src/modules/storage-adapter.js) | `loadState()`, `saveState()`, `resetState()`, `syncWithSupabase()`, `exportProjectBundle()` | Menyimpan dan memuat state proyek secara *hybrid* (sinkronisasi ke tabel PostgreSQL **Supabase** jika env tersedia, dengan *fallback* instan ke `localStorage`), serta mengekspor paket spesifikasi JSON/SQL untuk deployment klien. |
| **`BriefIntakeModule`** | [`src/modules/brief-intake.js`](file:///d:/APLIKASI/Project%20Ane/tuntungid/src/modules/brief-intake.js) | `getSectorPresets()`, `applyPresetToBrief()`, `validateBriefStep()`, `saveBriefDraft()`, `submitClientBrief()` | Mengelola prasetel 4 sektor bisnis, validasi 6 poin *Client Brief*, pengisian jadwal *Sesi Audit 30 Menit*, dan pembuatan proyek baru pada Tahap 1. |
| **`AgreementScopeModule`** | [`src/modules/agreement-scope.js`](file:///d:/APLIKASI/Project%20Ane/tuntungid/src/modules/agreement-scope.js) | `getTermsCatalog()`, `evaluateScopeStatus()`, `signTermsAndLockScope()`, `simulateAddonImpact()`, `submitAddonRequest()` | Memastikan seluruh 5 poin T&C disetujui sebelum *Scope Baseline* terkunci, serta memisahkan tiket perbaikan bug gratis (Garansi 30 Hari) dari permintaan fitur tambahan (*Add-on*). |
| **`ProjectLifecycleModule`** | [`src/modules/project-lifecycle.js`](file:///d:/APLIKASI/Project%20Ane/tuntungid/src/modules/project-lifecycle.js) | `listProjects()`, `getProjectDetail()`, `advanceProjectStage()`, `toggleOwnershipItem()`, `getPowerDuoWorkspaceSummary()` | Mengawal transisi 5 tahap metode kerja (menolak masuk ke Tahap 3 bila T&C belum ditandatangani), menghitung mundur garansi 30 hari pasca-rilis, dan memverifikasi 100% kepemilikan data/server klien. |

---

## 3. Skema Database Gratis (Supabase PostgreSQL / Cloudflare D1)

Disiapkan file migrasi siap pakai pada `supabase/schema.sql` dengan 3 tabel inti:
1. `client_briefs`: Menyimpan 6 poin *Client Brief* dan jadwal *Sesi Audit Gratis 30 Menit*.
2. `projects`: Menyimpan status tahapan proyek (1 s/d 5), status tanda tangan 5 poin T&C, *Scope Baseline*, checklist kepemilikan data 100% klien, dan tanggal mulai garansi 30 hari.
3. `scope_requests`: Menyimpan riwayat tiket garansi bug (`Rp 0`) dan pengajuan fitur tambahan (*Add-on*).

---

## 4. Kepatuhan Desain & Kualitas (`AGENTS.md` & `antislop`)

- **Design Read & Three Dials**:
  - **Landing Page (`Persuade`)**: `ENERGY 2 / RHYTHM 2 / MOTION 2` (Komposisi ChronoTask yang bersih, kartu ber-radius lembut di atas kanvas `#F6FAF8`, dan transisi fokus yang halus).
  - **Dashboard Workspace (`Operate`)**: `ENERGY 1 / RHYTHM 1 / MOTION 1` (Tata letak operasional tenang dengan angka `tabular-nums`, hierarki jelas, dan aksi spesifik).
- **Kepatuhan Kontras WCAG AA (`R-25`)**: Seluruh pasangan warna teks (`#0E3A2F`, `#355E52`) di atas latar (`#FFFFFF`, `#F6FAF8`, `#E8F4EE`, `#FEF5D9`) dan teks putih di atas `#187941` telah teruji lolos standar WCAG AA.
- **Kepatuhan Copywriting (`R-02`, `R-15`, `R-17`, `R-18`)**: Nol karakter em-dash, nol testimoni/nama fiktif, nol klaim persentase karangan, dan label tombol yang spesifik menjelaskan aksi.
