"use client";

import { useActionState, useRef, useEffect } from "react";
import { createClientAction } from "./actions.js";

const field = "w-full min-h-[48px] rounded-xl bg-soft px-4 text-base";

export function CreateClientForm() {
  const [state, formAction, pending] = useActionState(createClientAction, null);
  const formRef = useRef(null);

  useEffect(() => {
    if (state?.ok) formRef.current?.reset();
  }, [state]);

  return (
    <form ref={formRef} action={formAction} className="grid gap-3 sm:grid-cols-2" noValidate>
      <div>
        <label htmlFor="full_name" className="block text-sm font-semibold mb-1.5">Nama klien</label>
        <input id="full_name" name="full_name" required className={field} />
      </div>
      <div>
        <label htmlFor="company" className="block text-sm font-semibold mb-1.5">Usaha atau instansi</label>
        <input id="company" name="company" className={field} />
      </div>
      <div>
        <label htmlFor="email" className="block text-sm font-semibold mb-1.5">Email login</label>
        <input id="email" name="email" type="email" required autoComplete="off" className={field} />
      </div>
      <div>
        <label htmlFor="password" className="block text-sm font-semibold mb-1.5">Kata sandi sementara</label>
        <input id="password" name="password" type="text" required minLength={8} autoComplete="off" className={field} />
      </div>
      <div className="sm:col-span-2">
        <label htmlFor="title" className="block text-sm font-semibold mb-1.5">Nama proyek pertama</label>
        <input id="title" name="title" required className={field} />
      </div>
      {state?.error && (
        <p role="alert" className="sm:col-span-2 rounded-xl bg-danger-bg p-3 text-sm font-medium text-danger">{state.error}</p>
      )}
      {state?.ok && (
        <p role="status" className="sm:col-span-2 rounded-xl bg-ok-bg p-3 text-sm font-medium">{state.message}</p>
      )}
      <div className="sm:col-span-2">
        <button type="submit" disabled={pending} className="min-h-[48px] px-5 rounded-xl bg-brand text-white font-semibold hover:bg-brand-hover">
          {pending ? "Membuat akun..." : "Buat Akun Klien"}
        </button>
      </div>
    </form>
  );
}

