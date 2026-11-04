import Link from "next/link";
import { Logo } from "../components/logo.jsx";
import { StageTracker } from "../components/stage-tracker.jsx";
import { STAGES } from "../lib/stages.js";

const WA_TEXT = "Halo Tuntung.id, saya ingin menjadwalkan audit gratis 30 menit untuk alur kerja kami.";

function waLink() {
  let num = (process.env.NEXT_PUBLIC_WHATSAPP_NUMBER || "").replace(/\D/g, "");
  if (num.startsWith("0")) {
    num = "62" + num.slice(1);
  }
  return `https://wa.me/${num}?text=${encodeURIComponent(WA_TEXT)}`;
}

const SERVICES = [
  {
    title: "Audit Gratis 30 Menit",
    text: "Kami bedah alur kerja Anda dan petakan apa yang bisa diotomatisasi."
  },
  {
    title: "Aplikasi Kustom dan Otomasi",
    text: "Web app, dashboard, dan integrasi yang dibuat sesuai cara kerja tim Anda."
  },
  {
    title: "Pendampingan dan Garansi",
    text: "Pelatihan tim, serah terima penuh, dan garansi bug 30 hari."
  }
];

export default function LandingPage() {
  const wa = waLink();
  return (
    <div className="mx-auto w-full max-w-[1200px] px-4 sm:px-6">
      <header className="flex items-center justify-between gap-3 py-3">
        <Logo />
        <nav aria-label="Navigasi utama" className="hidden md:flex items-center gap-8 text-sm font-medium">
          <a href="#layanan" className="min-h-[44px] inline-flex items-center hover:text-brand">Layanan</a>
          <a href="#metode" className="min-h-[44px] inline-flex items-center hover:text-brand">Metode Kerja</a>
          <a href="#dashboard" className="min-h-[44px] inline-flex items-center hover:text-brand">Dashboard</a>
        </nav>
        <div className="flex items-center gap-2">
          <Link href="/masuk" className="min-h-[44px] px-3 inline-flex items-center text-sm font-semibold hover:text-brand">
            Masuk
          </Link>
          <a
            href={wa}
            target="_blank"
            rel="noreferrer"
            className="min-h-[44px] px-4 hidden sm:inline-flex items-center rounded-xl bg-white text-sm font-semibold hover:bg-soft"
          >
            Jadwalkan Audit
          </a>
        </div>
      </header>

      <main>
        <section className="dot-field relative overflow-hidden rounded-[28px] px-5 py-16 sm:py-24 xl:py-36 text-center">
          <div className="hidden xl:block">
            <div data-ui className="float-card drift absolute left-8 top-10 w-64 p-4 text-left">
              <p className="text-sm font-semibold">Tahap proyek</p>
              <div className="mt-3"><StageTracker stage={3} compact /></div>
              <p className="text-sm text-ink-2 mt-2.5">Tahap 3 dari 5: Eksekusi dan Development</p>
            </div>
            <div data-ui className="float-card drift absolute right-8 top-14 w-60 p-4 text-left [animation-delay:-2s]">
              <p className="text-sm font-semibold">Permintaan Anda</p>
              <div className="mt-3 flex flex-wrap gap-2 text-sm font-medium">
                <span className="px-2.5 py-1 rounded-lg bg-ok-bg text-brand">Revisi</span>
                <span className="px-2.5 py-1 rounded-lg bg-soft">Fitur Tambahan</span>
              </div>
              <p className="text-sm text-ink-2 mt-2.5">Balasan admin muncul di sini.</p>
            </div>
            <div data-ui className="float-card drift absolute left-14 bottom-10 w-60 p-4 text-left [animation-delay:-4s]">
              <p className="text-sm font-semibold">File serah terima</p>
              <ul className="mt-2.5 space-y-1.5 text-sm text-ink-2">
                <li>Kode sumber aplikasi</li>
                <li>Panduan penggunaan</li>
              </ul>
            </div>
            <div data-ui className="float-card drift absolute right-14 bottom-12 w-56 p-4 text-left [animation-delay:-1s]">
              <p className="text-sm font-semibold">Jadwal</p>
              <p className="text-sm text-ink-2 mt-2">Tanggal mulai dan target rilis selalu terlihat.</p>
            </div>
          </div>

          <h1 className="rise relative mx-auto text-[clamp(2rem,5.2vw,3.75rem)] font-bold leading-[1.04]">
            Gawi Manuntung,
            <span className="block text-ink/45">Supaya Untung</span>
          </h1>
          <p className="rise relative mx-auto mt-5 max-w-[44ch] text-base sm:text-lg text-ink-2 [animation-delay:80ms]">
            Kami membuat aplikasi dan web app untuk bisnis Anda, lalu Anda pantau prosesnya di dashboard.
          </p>
          <div className="rise relative mt-8 [animation-delay:160ms]">
            <a
              href={wa}
              target="_blank"
              rel="noreferrer"
              className="min-h-[48px] px-6 inline-flex items-center rounded-xl bg-brand text-white font-semibold hover:bg-brand-hover"
            >
              Jadwalkan Audit Gratis
            </a>
          </div>
        </section>

        <section id="layanan" className="scroll-mt-6 py-20 sm:py-24 grid gap-10 md:grid-cols-[1fr_1.6fr] md:gap-16">
          <h2 className="text-[clamp(1.75rem,3.6vw,2.5rem)] font-bold md:sticky md:top-8 md:self-start">
            Yang kami kerjakan
          </h2>
          <ul className="space-y-8">
            {SERVICES.map((s) => (
              <li key={s.title}>
                <h3 className="font-display font-semibold text-[clamp(1.35rem,2.4vw,1.75rem)] leading-tight">{s.title}</h3>
                <p className="text-ink-2 mt-2 max-w-[52ch]">{s.text}</p>
              </li>
            ))}
          </ul>
        </section>

        <section id="metode" className="scroll-mt-6 rounded-[28px] bg-white px-5 py-14 sm:px-10 sm:py-16">
          <h2 className="text-center text-[clamp(1.75rem,3.6vw,2.5rem)] font-bold">Lima tahap sampai tuntas</h2>
          <ol className="mt-10 grid gap-3 sm:grid-cols-2 md:grid-cols-5">
            {STAGES.map((s) => (
              <li key={s.number} className="rounded-2xl bg-soft p-4">
                <span className="grid place-items-center size-8 rounded-full bg-ink text-white text-sm font-semibold tabular-nums">
                  {s.number}
                </span>
                <h3 className="font-display font-semibold text-base mt-3 leading-snug">{s.name}</h3>
                <p className="text-sm text-ink-2 mt-1.5">{s.note}</p>
              </li>
            ))}
          </ol>
        </section>

        <section id="dashboard" className="scroll-mt-6 py-20 sm:py-24">
          <h2 className="text-center text-[clamp(1.75rem,3.6vw,2.5rem)] font-bold">Pantau proyek dari satu dashboard</h2>
          <p className="text-center text-ink-2 mt-3">Contoh tampilan Dashboard Klien.</p>
          <div className="mt-10 rounded-[28px] bg-brand p-3 sm:p-6">
            <div data-ui className="float-card grid md:grid-cols-[200px_1fr] overflow-hidden">
              <aside className="hidden md:block bg-soft p-4">
                <Logo href="/" />
                <ul className="mt-6 space-y-1 text-sm font-medium">
                  <li className="rounded-xl bg-white px-3 py-2.5">Proyek</li>
                  <li className="px-3 py-2.5 text-ink-2">File</li>
                  <li className="px-3 py-2.5 text-ink-2">Permintaan</li>
                </ul>
              </aside>
              <div className="p-5 sm:p-6">
                <p className="text-sm text-ink-2">Proyek Anda</p>
                <h3 className="font-display font-bold text-xl mt-1">[Nama Proyek Klien]</h3>
                <div className="mt-5"><StageTracker stage={3} /></div>
                <div className="mt-5 grid gap-3 sm:grid-cols-2">
                  <div className="rounded-2xl bg-soft p-4">
                    <p className="text-sm font-semibold">Jadwal</p>
                    <p className="text-sm text-ink-2 mt-1">Mulai dan target rilis</p>
                  </div>
                  <div className="rounded-2xl bg-soft p-4">
                    <p className="text-sm font-semibold">Kirim permintaan</p>
                    <p className="text-sm text-ink-2 mt-1">Revisi atau fitur tambahan</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="kontak" className="scroll-mt-6 rounded-[28px] bg-ink px-6 py-14 text-center text-white sm:py-20">
          <h2 className="mx-auto max-w-[26ch] text-[clamp(1.5rem,3.6vw,2.5rem)] font-bold">
            Masih ada yang dicatat manual?
          </h2>
          <p className="mx-auto mt-4 max-w-[46ch] text-white/80">
            Ceritakan alurnya di sesi audit 30 menit. Gratis, tanpa kewajiban lanjut.
          </p>
          <a
            href={wa}
            target="_blank"
            rel="noreferrer"
            className="mt-8 min-h-[48px] px-6 inline-flex items-center rounded-xl bg-gold text-ink font-semibold hover:bg-white"
          >
            Chat WhatsApp Sekarang
          </a>
        </section>
      </main>

      <footer className="flex flex-wrap items-center justify-between gap-3 py-8 text-sm text-ink-2">
        <span>© 2026 Tuntung.id</span>
        <Link href="/masuk" className="min-h-[44px] inline-flex items-center font-semibold text-ink hover:text-brand">
          Masuk ke Dashboard
        </Link>
      </footer>
    </div>
  );
}
