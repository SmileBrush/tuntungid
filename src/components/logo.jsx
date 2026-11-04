import Link from "next/link";

export function Logo({ href = "/", light = false }) {
  return (
    <Link href={href} className="inline-flex items-center gap-2.5 min-h-[44px]" aria-label="Tuntung.id, ke beranda">
      <svg width="34" height="34" viewBox="0 0 34 34" aria-hidden="true">
        <rect x="2" y="3" width="30" height="10" rx="4" fill="#187941" />
        <rect x="12" y="3" width="10" height="28" rx="4" fill="#22a45d" />
        <rect x="23" y="16" width="9" height="9" rx="3" fill="#f4b41a" />
      </svg>
      <span className={`font-display font-bold text-xl ${light ? "text-white" : "text-ink"}`}>Tuntung.id</span>
    </Link>
  );
}

