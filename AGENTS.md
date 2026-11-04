# AGENTS.md: Protokol Kerja & Orkestrasi Skill

Dokumen ini adalah acuan utama bagi AI Agent dalam merancang, membangun, mengaudit, dan memelihara aplikasi pada repositori ini. Seluruh pekerjaan wajib mengikuti 16 skill yang terpasang di `.agents/skills/`.oke l

---

## 1. Peta Ekosistem Skill (`.agents/skills/`)

Seluruh skill dikelompokkan ke dalam 5 pilar sesuai siklus pengembangan perangkat lunak:

### Pilar A: Perencanaan, Ideasi & Penajaman Spesifikasi
1. **[`brainstorming`](.agents/skills/brainstorming/SKILL.md)**: Gerbang wajib sebelum menulis kode atau memanggil skill implementasi. Mengklasifikasikan setiap tugas ke dalam 3 jalur (`Spike`, `Bounded`, atau `Architectural`) dan mewajibkan persetujuan desain dari pengguna (*Hard Gate*).
2. **[`grill-me`](.agents/skills/grill-me/SKILL.md)**: Sesi tanya-jawab mendalam untuk menguji asumsi, menemukan celah logika, dan mempertajam rencana sebelum eksekusi.
3. **[`find-skills`](.agents/skills/find-skills/SKILL.md)**: Pencarian dan instalasi skill tambahan melalui `npx skills` jika dibutuhkan kapabilitas domain spesifik baru.

### Pilar B: Arsitektur Kode & Pemetaan Struktural
4. **[`codebase-design`](.agents/skills/codebase-design/SKILL.md)**: Panduan merancang **Deep Modules** (*Small Interface + Deep Implementation*) pada **Seam** yang tepat. Mengatur kosakata arsitektur (`Module`, `Interface`, `Implementation`, `Adapter`, `Depth`, `Seam`, `Leverage`, `Locality`) dan prinsip *testability*.
5. **[`codebase-memory`](.agents/skills/codebase-memory/SKILL.md)**: Penggunaan 15 tool MCP `codebase-memory` (`list_projects`, `index_status`, `search_graph`, `trace_path`, `detect_changes`, `query_graph`, `check_index_coverage`, dll.) untuk menelusuri arsitektur, dependensi, dan dampak perubahan secara presisi.

### Pilar C: Art Direction & Sistem Desain UI/UX
6. **[`design-taste-frontend`](.agents/skills/design-taste-frontend/SKILL.md)** (*tasteskill v2*): Sistem *art direction* berbasis riset 247 situs kurasi. Menyediakan alur terpisah untuk **Page** (halaman publik/marketing) dan **App Screen** (`--app`: dashboard, admin, pengaturan, tabel kerja) beserta script otomatis (`draw.mjs`, `assets.mjs`, `lint.mjs`, `inspect.mjs`, `scenes.mjs`).
7. **[`impeccable`](.agents/skills/impeccable/SKILL.md)** (*v4.1.3*): Kerangka kerja *design director* dengan 4 mode permukaan (**Persuade**, **Operate**, **Read**, **Experience**), pemuatan konteks via `scripts/context.mjs` (`PRODUCT.md` & `DESIGN.md`), standar dasar [`reference/craft-floor.md`](.agents/skills/impeccable/reference/craft-floor.md), dan 22 sub-command (`shape`, `init`, `document`, `extract`, `critique`, `audit`, `polish`, `harden`, `distill`, `clarify`, `adapt`, `optimize`, dll.).
8. **[`frontend-design`](.agents/skills/frontend-design/SKILL.md)**: Prinsip desain intensional untuk menciptakan karakter visual yang khas, merancang sistem token ringkas, menentukan satu *signature element* yang berkesan, dan menulis UX copy dari sudut pandang pengguna.

### Pilar D: Filter Kualitas, Responsivitas, Aksesibilitas & Kebersihan Kode (`antislop` Suite)
9. **[`antislop`](.agents/skills/antislop/SKILL.md)**: Filter utama pencegah *AI slop* yang memuat 5 standar *Craftsmanship* (`C-1` s/d `C-5`), 40 aturan wajib (`R-01` s/d `R-40` yang terbagi atas *Hard Gate*, *Purpose-Gate*, dan *Quality Locks*), *Three Dials* (`ENERGY`, `RHYTHM`, `MOTION`), serta **Mandatory Delivery Gate**.
10. **[`antislop-ui`](.agents/skills/antislop-ui/SKILL.md)**: Aturan visual antarmuka untuk warna, komposisi, komponen, layar aplikasi/dashboard, gerak (*motion*), dan performa elemen media.
11. **[`antislop-layoutmobile`](.agents/skills/antislop-layoutmobile/SKILL.md)**: Standar *responsive reflow* dari layar ponsel, tablet/laptop kecil (600-1024px), hingga desktop, termasuk skala tipografi fluida, pencegahan *horizontal overflow*, ukuran *tap target* minimal `44x44px`, dan pola navigasi mobile.
12. **[`antislop-human`](.agents/skills/antislop-human/SKILL.md)**: Aksesibilitas nyata mencakup pengecekan rasio kontras (`contrast-check.py` / WCAG AA), navigasi keyboard penuh, indikator fokus, larangan umpan balik berbasis warna saja, *zoom* teks 200%, dan dukungan `prefers-reduced-motion`.
13. **[`antislop-code`](.agents/skills/antislop-code/SKILL.md)**: Kebersihan komentar kode. Menghapus komentar dekoratif, pengulangan logika kode, dan TODO kabur, serta hanya mempertahankan komentar singkat (1-2 baris) yang menjelaskan alasan teknis penting tanpa mengubah logika kode.

### Pilar E: Copywriting, Microcopy & Kualitas Teks
14. **[`antislop-copywriting`](.agents/skills/antislop-copywriting/SKILL.md)**: Standar penulisan teks UI, headline, dan CTA agar spesifik, jujur, bebas *buzzword* AI, bebas kalimat pasif tanpa pelaku, dan bebas tanda pisah em-dash.
15. **[`avoid-ai-writing`](.agents/skills/avoid-ai-writing/SKILL.md)**: Audit dan penulisan ulang teks (`rewrite`, `detect`, `edit`) berdasarkan tingkat keparahan (`P0`, `P1`, `P2`) dengan tetap menjaga kesetiaan fakta sumber (*source fidelity*).
16. **[`stop-slop`](.agents/skills/stop-slop/SKILL.md)**: Pembersihan prosa dari basa-basi pembuka, struktur kontras klise, kata keterangan berlebih, dan ritme kalimat yang monoton (skor kualitas minimal 35/50).

---

## 2. Alur Kerja Wajib (End-to-End Workflow)

Setiap tugas wajib mengikuti urutan tahapan di bawah ini. Jangan melompati tahap perencanaan menuju penulisan kode.

### Tahap 1: Klasifikasi & Brainstorming (Hard Gate)
1. Baca [`.agents/skills/brainstorming/SKILL.md`](.agents/skills/brainstorming/SKILL.md).
2. Klasifikasikan permintaan pengguna secara eksplisit di awal respons ke dalam salah satu jalur:
   - **Spike**: Eksplorasi kelayakan teknis singkat.
   - **Bounded**: Perubahan terarah pada alur kode yang sudah ada di repositori.
   - **Architectural**: Proyek baru, subsistem baru, atau perombakan struktur antarmuka. (Proyek baru dari nol selalu masuk jalur **Architectural**).
3. Jika spesifikasi masih memiliki banyak cabang keputusan, tawarkan atau jalankan pola wawancara dari [`grill-me`](.agents/skills/grill-me/SKILL.md) (satu pertanyaan per pesan).
4. Untuk jalur **Architectural**, ajukan 2-3 pendekatan beserta *trade-off*, presentasikan desain secara bertahap, tulis spesifikasi ke `docs/superpowers/specs/YYYY-MM-DD-<topik>-design.md`, dan **tunggu persetujuan eksplisit pengguna** sebelum mulai mengimplementasikan kode.

### Tahap 2: Pemetaan & Perancangan Arsitektur Kode
1. **Saat Codebase Sudah Memiliki Kode**:
   - Jalankan alur [`codebase-memory`](.agents/skills/codebase-memory/SKILL.md): periksa `list_projects` / `index_status`, gunakan `search_graph` dan `trace_path` untuk memetakan hubungan fungsi, serta panggil `check_index_coverage` sebelum mengambil kesimpulan struktural.
2. **Saat Merancang Modul & Antarmuka Baru**:
   - Terapkan prinsip [`codebase-design`](.agents/skills/codebase-design/SKILL.md):
     - Gunakan terminologi baku: `Module`, `Interface`, `Implementation`, `Adapter`, `Depth`, `Seam`, `Leverage`, dan `Locality`.
     - Rancang **Deep Modules**: sembunyikan kompleksitas bisnis di balik `Interface` yang ringkas dan jelas.
     - Desain untuk kemudahan pengujian (*testability*): terima dependensi melalui parameter (jangan menginstansiasi dependensi eksternal secara tersembunyi di dalam fungsi) dan utamakan pengembalian nilai dibanding *side effects*.
     - Jangan membuat `Seam` / abstraksi hipotesis jika hanya ada satu implementasi dan belum ada kebutuhan variasi nyata (*YAGNI*).

### Tahap 3: Orkestrasi Desain UI/UX (Menyelaraskan `impeccable`, `design-taste-frontend`, `frontend-design`, & `antislop`)
Agar ketiga skill desain dan filter `antislop` bekerja selaras tanpa saling bertabrakan, ikuti aturan orkestrasi berikut:

1. **Dokumen Arah Produk & Desain (`PRODUCT.md` & `DESIGN.md`)**:
   - Jadikan `PRODUCT.md` dan `DESIGN.md` sebagai sumber acuan utama identitas produk (sesuai `antislop` R-37 dan `impeccable`).
   - Sebelum membangun UI, pastikan arah desain telah ditetapkan (atau gunakan perintah `init` / `shape` pada [`impeccable`](.agents/skills/impeccable/SKILL.md) untuk mendefinisikannya bersama pengguna).
2. **Menentukan Jenis Permukaan (Surface Type)**:
   - **Layar Aplikasi (`Operate` / `--app`)**: Dashboard, panel admin, pengaturan, tabel data, kasir, form kerja.
     - Baca [`.agents/skills/design-taste-frontend/references/app-screens.md`](.agents/skills/design-taste-frontend/references/app-screens.md) dan [`.agents/skills/impeccable/reference/operate.md`](.agents/skills/impeccable/reference/operate.md).
     - Bangun tata letak berdasarkan **keputusan utama yang harus diambil pengguna di layar tersebut**, bukan *template* standar (sidebar + 4 kartu angka + grafik dekoratif + tabel generik).
   - **Halaman Publik (`Persuade` / `Experience` / `Read`)**: Landing page, halaman produk, dokumentasi, portofolio.
     - Gunakan alur [`design-taste-frontend`](.agents/skills/design-taste-frontend/SKILL.md) (`scripts/draw.mjs`) dan prinsip [`frontend-design`](.agents/skills/frontend-design/SKILL.md) untuk menghasilkan komposisi yang berkarakter kuat dan memiliki satu *live interactive element* yang relevan dengan produk.
3. **Deklarasi Mode `antislop` & Design Read**:
   - Ikuti resolusi mode pada [`antislop`](.agents/skills/antislop/SKILL.md) (`during` atau `after`). Saat membangun aplikasi dari awal, gunakan mode **DURING** (atau tanyakan kepada pengguna jika belum ditetapkan pada sesi tersebut).
   - Deklarasikan *Design Read* beserta nilai *Three Dials* (`ENERGY 1-3 / RHYTHM 1-3 / MOTION 1-3`) sebelum membangun komponen UI.
4. **Resolusi Aturan Visual Ketat**:
   - Jika tidak ada instruksi khusus dari pengguna di `DESIGN.md`, patuhi batas paling ketat dari gabungan `design-taste-frontend` dan `antislop`:
     - **Palet Warna**: Maksimal 2-3 warna inti (ground, surface, ink) + 1 warna aksen yang hanya muncul pada elemen aksi utama (`R-29`). Dilarang memakai gradasi biru-ungu generik (`R-01`) atau palet klise tanpa alasan brand.
     - **Tipografi**: Maksimal 2 keluarga font (`design-taste-frontend`). Pilih font berdasarkan karakter produk dan catat alasannya (`R-06`). Headline maksimal 2 baris pada setiap lebar layar.
     - **Ornamen**: Dilarang memasang *eyebrow pill badge* di atas `H1` yang hanya mengulang isi judul (`R-09`), dilarang menaruh panah dekoratif pada setiap tombol (`R-08`), dilarang memakai *glow* atau *glassmorphism* berlebihan (`R-10`, `R-13`), dan dilarang memakai nomor indeks dekoratif (`01 / 02 / 03`) kecuali urutan benar-benar bermakna.

### Tahap 4: Standar Implementasi Responsif, Aksesibilitas, Teks & Kode
Saat menulis kode komponen dan logika aplikasi, terapkan keempat skill spesialis berikut secara bersamaan:

1. **Responsivitas Lintas Layar ([`antislop-layoutmobile`](.agents/skills/antislop-layoutmobile/SKILL.md))**:
   - Desain tampilan mobile sebagai komposisi tersendiri yang melakukan *reflow*, bukan sekadar tampilan desktop yang diperkecil (`R-03`).
   - Pastikan rentang layar menengah (tablet & laptop kecil 600-1024px) memiliki tata letak yang proporsional (tidak terjebak pada *two-state layout* yang renggang atau terlalu sempit).
   - Gunakan ukuran fluida (`clamp()`) untuk tipografi, `dvh` (bukan `100vh`) bila memerlukan tinggi layar penuh, serta pastikan **nol horizontal overflow**.
   - Semua target sentuh (*tap targets*) minimal berukuran `44x44px` dengan jarak antar-elemen yang aman.
2. **Aksesibilitas & Interaksi Manusia ([`antislop-human`](.agents/skills/antislop-human/SKILL.md))**:
   - Uji setiap pasangan warna teks dan latar menggunakan rumus/script `.agents/skills/antislop-human/contrast-check.py` (minimal `4.5:1` untuk teks normal, `3:1` untuk teks besar 18px+ dan batas komponen interaktif, sesuai `R-25`).
   - Gunakan elemen HTML semantik asli (`<button>` untuk aksi, `<a href>` untuk navigasi nyata; dilarang memakai `<div onClick>`). Pastikan setiap kontrol aktif memiliki `cursor: pointer`, label yang jelas (`<label>` atau `aria-label`), serta *focus indicator* yang terlihat jelas (`R-32`, `R-39`).
   - Sediakan ketiga *state* wajib pada setiap tampilan data: **Empty state** (jelaskan mengapa kosong + tombol aksi untuk mengisinya), **Loading state** (dengan teks konteks), dan **Error state** (jelaskan apa yang gagal + cara mengatasinya, bukan hanya warna merah) (`R-27`).
   - Hormati `prefers-reduced-motion: reduce` pada seluruh animasi (`R-39`).
3. **Copywriting & Microcopy ([`antislop-copywriting`](.agents/skills/antislop-copywriting/SKILL.md), [`avoid-ai-writing`](.agents/skills/avoid-ai-writing/SKILL.md), [`stop-slop`](.agents/skills/stop-slop/SKILL.md))**:
   - **Dilarang keras** menggunakan karakter em-dash (`—`) pada teks UI maupun prosa yang ditulis agen (`R-02`). Gunakan tanda koma, titik, titik dua, atau tanda kurung.
   - **Dilarang keras** mengarang angka statistik, metrik kenaikan (`+12% minggu ini`), testimoni, nama pengguna fiktif (`John Doe`, `Sarah Chen`), atau klaim keamanan palsu (`R-17`, `R-18`, `R-36`, `R-38`). Gunakan data nyata dari sistem atau *placeholder* jujur seperti `[REAL DATA]` / `nama@contoh.com`.
   - Gunakan label tombol/CTA yang menjelaskan aksi spesifik (misalnya *"Buat Invoice Baru"*, *"Simpan Perubahan"*), bukan label generik (*"Get Started"*, *"Learn More"*, *"Submit"*) (`R-15`).
   - Hindari kosakata klise AI (*seamless, elevate, unlock, empower, cutting-edge, revolutionary*) serta kalimat pasif tanpa subjek.
4. **Kebersihan Komentar Kode ([`antislop-code`](.agents/skills/antislop-code/SKILL.md))**:
   - Jangan menulis komentar dekoratif (`// =======`), komentar yang mengulang nama fungsi/variabel, komentar narasi langkah (`// Step 1: ...`), atau emoji di dalam komentar.
   - Tulis komentar hanya jika ada informasi yang tidak terlihat langsung dari kode (alasan bisnis, batasan protokol/API, *workaround*, atau *edge case*), maksimal 1-2 baris dalam kalimat biasa.

### Tahap 5: Verifikasi & Delivery Gate (Wajib Sebelum Selesai)
Sebelum menyatakan pekerjaan selesai atau menyerahkan hasil kepada pengguna:
1. **Jalankan & Uji Aplikasi (`R-35`)**:
   - Jalankan *build* / server aplikasi dan periksa konsol dari error.
   - Klik dan uji setiap elemen interaktif satu per satu (tombol, tautan, form, modal, tab, menu mobile, dan *theme toggle* jika ada).
   - Jika bekerja pada halaman web dengan Node 22+ dan browser tersedia, jalankan pemeriksa otomatis dari `design-taste-frontend` (`node .agents/skills/design-taste-frontend/scripts/lint.mjs` & `inspect.mjs`) atau `impeccable` (`context.mjs` / `audit`).
2. **Jalankan Checklist & Delivery Gate**:
   - Evaluasi seluruh blok **Delivery Gate** pada [`.agents/skills/antislop/SKILL.md`](.agents/skills/antislop/SKILL.md) (*Block 1: Hard Gate*, *Block 2: Purpose-Gate*, *Block 3: Liveliness*, *Block 4: Craftsmanship & Quality Locks*) beserta checklist dari sub-skill yang relevan (`antislop-ui`, `antislop-layoutmobile`, `antislop-human`, `antislop-copywriting`, `antislop-code`).
   - Pastikan setiap keputusan desain utama memiliki alasan tertulis satu baris (`R-31`).
   - Laporkan hasil verifikasi klik nyata dan status **PASS/FAIL** secara jujur kepada pengguna. Jangan pernah menyerahkan pekerjaan yang masih memiliki status **FAIL**.

---

## 3. Matriks Pemicu Skill (Quick Routing Table)

| Tugas / Kondisi | Skill yang Wajib Dimuat |
| :--- | :--- |
| Memulai proyek baru, fitur baru, atau perubahan perilaku | `brainstorming` (+ `grill-me` bila butuh eksplorasi mendalam) |
| Menelusuri kode, mencari pemanggil fungsi, analisis dampak | `codebase-memory` |
| Merancang modul, *interface*, *seam*, & struktur pengujian | `codebase-design` |
| Menetapkan konteks produk (`PRODUCT.md` / `DESIGN.md`) | `impeccable` (`init`, `shape`, `document`), `antislop` (`R-37`) |
| Membangun halaman publik (*landing page*, *marketing*, *portfolio*) | `antislop`, `design-taste-frontend`, `frontend-design`, `antislop-ui`, `antislop-layoutmobile`, `antislop-human` |
| Membangun layar aplikasi (*dashboard*, *admin*, *form*, *settings*) | `antislop`, `design-taste-frontend` (`references/app-screens.md`), `impeccable` (`Operate` mode), `antislop-ui`, `antislop-layoutmobile`, `antislop-human` |
| Memoles, mengaudit, atau memperbaiki UI yang sudah ada | `impeccable` (`critique`, `audit`, `polish`, `harden`, `distill`, `clarify`, `adapt`, `optimize`), `antislop` |
| Menulis teks UI, headline, CTA, pesan error, atau dokumentasi | `antislop`, `antislop-copywriting`, `avoid-ai-writing`, `stop-slop` |
| Menulis atau merapikan kode dan komentar kode | `codebase-design`, `antislop-code` |
| Mencari skill baru dari ekosistem | `find-skills` |

