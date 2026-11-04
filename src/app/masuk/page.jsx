import Link from "next/link";
import { Logo } from "../../components/logo.jsx";
import { LoginForm } from "./login-form.jsx";

export const metadata = { title: "Masuk | Tuntung.id" };

export default function MasukPage() {
  return (
    <main className="dot-field min-h-dvh grid place-items-center px-4 py-10">
      <div data-ui className="float-card w-full max-w-[420px] p-6 sm:p-8">
        <Logo />
        <h1 className="font-display font-bold text-2xl mt-4">Masuk ke dashboard</h1>
        <p className="text-ink-2 mt-1">Akun klien dibuat oleh tim Tuntung.id.</p>
        <LoginForm />
        <Link href="/" className="mt-5 min-h-[44px] inline-flex items-center text-sm font-semibold text-ink-2 hover:text-brand">
          Kembali ke beranda
        </Link>
      </div>
    </main>
  );
}

