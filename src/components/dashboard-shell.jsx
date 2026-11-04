import Link from "next/link";
import { Logo } from "./logo.jsx";
import { logoutAction } from "../app/actions.js";

export function DashboardShell({ roleLabel, userName, nav, active, children }) {
  return (
    <div className="min-h-dvh md:grid md:grid-cols-[232px_1fr]">
      <aside className="hidden md:flex flex-col bg-white p-4 sticky top-0 h-dvh">
        <Logo href="/" />
        <p className="text-sm text-ink-2 mt-5 px-1">{roleLabel}</p>
        <nav aria-label="Menu dashboard" className="mt-2 flex flex-col gap-1">
          {nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              aria-current={item.key === active ? "page" : undefined}
              className={`min-h-[44px] px-3 rounded-xl inline-flex items-center justify-between text-sm font-semibold ${
                item.key === active ? "bg-ink text-white" : "text-ink hover:bg-soft"
              }`}
            >
              {item.label}
              {item.badge ? (
                <span className="ml-2 rounded-full bg-gold px-2 py-0.5 text-xs font-bold text-ink tabular-nums">{item.badge}</span>
              ) : null}
            </Link>
          ))}
        </nav>
        <div className="mt-auto">
          <p className="text-sm font-semibold px-1 truncate">{userName}</p>
          <form action={logoutAction}>
            <button type="submit" className="mt-2 w-full min-h-[44px] rounded-xl bg-soft text-sm font-semibold hover:bg-line">
              Keluar
            </button>
          </form>
        </div>
      </aside>

      <div className="min-w-0">
        <header className="md:hidden bg-white px-4 py-2 flex items-center justify-between gap-2">
          <Logo href="/" />
          <form action={logoutAction}>
            <button type="submit" className="min-h-[44px] px-4 rounded-xl bg-soft text-sm font-semibold">Keluar</button>
          </form>
        </header>
        <nav aria-label="Menu dashboard" className="md:hidden flex gap-2 overflow-x-auto px-4 py-2">
          {nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              aria-current={item.key === active ? "page" : undefined}
              className={`min-h-[44px] shrink-0 px-4 rounded-xl inline-flex items-center text-sm font-semibold ${
                item.key === active ? "bg-ink text-white" : "bg-white"
              }`}
            >
              {item.label}
              {item.badge ? <span className="ml-2 rounded-full bg-gold px-2 text-xs font-bold text-ink">{item.badge}</span> : null}
            </Link>
          ))}
        </nav>
        <main className="mx-auto w-full max-w-[1040px] px-4 py-5 sm:px-6 sm:py-8">{children}</main>
      </div>
    </div>
  );
}

export function ErrorBox({ title, hint }) {
  return (
    <div role="alert" className="rounded-2xl bg-danger-bg p-5 text-danger">
      <p className="font-display font-semibold">{title}</p>
      {hint && <p className="text-sm mt-1">{hint}</p>}
    </div>
  );
}

