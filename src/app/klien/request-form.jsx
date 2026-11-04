"use client";

import { useActionState, useRef, useEffect } from "react";
import { sendRequestAction } from "./actions.js";

export function RequestForm({ projectId }) {
  const [state, formAction, pending] = useActionState(sendRequestAction, null);
  const formRef = useRef(null);

  useEffect(() => {
    if (state?.ok) formRef.current?.reset();
  }, [state]);

  return (
    <form ref={formRef} action={formAction} className="space-y-3" noValidate>
      <input type="hidden" name="project_id" value={projectId} />
      <div>
        <label htmlFor="kind" className="block text-sm font-semibold mb-1.5">Jenis permintaan</label>
        <select id="kind" name="kind" defaultValue="revisi" className="w-full min-h-[48px] rounded-xl bg-soft px-3 text-base">
          <option value="revisi">Revisi</option>
          <option value="fitur_tambahan">Fitur Tambahan</option>
        </select>
      </div>
      <div>
        <label htmlFor="message" className="block text-sm font-semibold mb-1.5">Apa yang perlu diubah atau ditambah?</label>
        <textarea id="message" name="message" rows={4} required className="w-full rounded-xl bg-soft px-3 py-2.5 text-base" />
      </div>
      {state?.error && (
        <p role="alert" className="rounded-xl bg-danger-bg p-3 text-sm font-medium text-danger">{state.error}</p>
      )}
      {state?.ok && (
        <p role="status" className="rounded-xl bg-ok-bg p-3 text-sm font-medium">Permintaan terkirim. Admin akan membalas di sini.</p>
      )}
      <button type="submit" disabled={pending} className="min-h-[48px] px-5 rounded-xl bg-brand text-white font-semibold hover:bg-brand-hover">
        {pending ? "Mengirim..." : "Kirim Permintaan"}
      </button>
    </form>
  );
}

