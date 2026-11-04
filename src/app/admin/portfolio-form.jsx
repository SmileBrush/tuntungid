"use client";

import { useActionState, useRef, useEffect } from "react";
import { createPortfolioAction } from "./actions.js";

const field = "w-full min-h-[48px] rounded-xl bg-soft px-4 text-base";

export function PortfolioForm() {
  const [state, formAction, pending] = useActionState(createPortfolioAction, null);
  const formRef = useRef(null);

  useEffect(() => {
    if (state?.ok) formRef.current?.reset();
  }, [state]);

  return (
    <form ref={formRef} action={formAction} className="grid gap-3 sm:grid-cols-2" noValidate>
      <div>
        <label htmlFor="p_title" className="block text-sm font-semibold mb-1.5">
          Nama Proyek / Aplikasi
        </label>
        <input
          id="p_title"
          name="title"
          required
          placeholder="Misal: Sistem Kasir &amp; Inventori UMKM"
          className={field}
        />
      </div>

      <div>
        <label htmlFor="p_sector" className="block text-sm font-semibold mb-1.5">
          Sektor / Kategori Usaha
        </label>
        <input
          id="p_sector"
          name="sector"
          required
          placeholder="Misal: Ritel &amp; Distribusi, Pendidikan, Klinik"
          className={field}
        />
      </div>

      <div className="sm:col-span-2">
        <label htmlFor="p_summary" className="block text-sm font-semibold mb-1.5">
          Ringkasan Solusi (1 - 2 Kalimat)
        </label>
        <textarea
          id="p_summary"
          name="summary"
          rows={2}
          required
          placeholder="Jelaskan masalah manual apa yang diubah menjadi efisien oleh aplikasi ini..."
          className="w-full rounded-xl bg-soft px-4 py-2.5 text-base"
        />
      </div>

      <div>
        <label htmlFor="p_tech" className="block text-sm font-semibold mb-1.5">
          Teknologi / Stack
        </label>
        <input
          id="p_tech"
          name="tech_stack"
          defaultValue="Next.js + Supabase"
          placeholder="Misal: Next.js + PostgreSQL + WhatsApp API"
          className={field}
        />
      </div>

      <div>
        <label htmlFor="p_demo" className="block text-sm font-semibold mb-1.5">
          Tautan Demo / Web Aktif (Opsional)
        </label>
        <input
          id="p_demo"
          name="demo_url"
          type="url"
          placeholder="https://demo-app.com"
          className={field}
        />
      </div>

      <div className="sm:col-span-2">
        <label htmlFor="p_image" className="block text-sm font-semibold mb-1.5">
          URL Gambar Screenshot / Mockup
        </label>
        <input
          id="p_image"
          name="image_url"
          type="url"
          required
          placeholder="https://images.unsplash.com/... atau tautan gambar mockup"
          className={field}
        />
        <span className="text-xs text-ink-2 mt-1 block">
          Tempel URL gambar langsung (akhiran .jpg, .png, .webp atau URL gambar publik hosting gratis).
        </span>
      </div>

      {state?.error && (
        <p role="alert" className="sm:col-span-2 rounded-xl bg-danger-bg p-3 text-sm font-medium text-danger">
          {state.error}
        </p>
      )}

      {state?.ok && (
        <p role="status" className="sm:col-span-2 rounded-xl bg-ok-bg p-3 text-sm font-medium">
          {state.message}
        </p>
      )}

      <div className="sm:col-span-2">
        <button
          type="submit"
          disabled={pending}
          className="min-h-[48px] px-5 rounded-xl bg-brand text-white font-semibold hover:bg-brand-hover"
        >
          {pending ? "Menyimpan Portofolio..." : "Simpan &amp; Terbitkan Portofolio"}
        </button>
      </div>
    </form>
  );
}
