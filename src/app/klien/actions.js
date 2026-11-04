"use server";

import { revalidatePath } from "next/cache";
import { getSessionUser } from "../../lib/supabase/server.js";
import { resolveRole } from "../../lib/access.js";

export async function sendRequestAction(_prev, formData) {
  const { supabase, user } = await getSessionUser();
  if (resolveRole(user) !== "client") return { error: "Sesi berakhir. Masuk lagi untuk mengirim permintaan." };

  const projectId = String(formData.get("project_id") || "");
  const kind = String(formData.get("kind") || "");
  const message = String(formData.get("message") || "").trim();
  if (!["revisi", "fitur_tambahan"].includes(kind)) return { error: "Pilih jenis permintaan." };
  if (message.length < 5) return { error: "Tulis permintaan minimal 5 karakter." };

  const { error } = await supabase.from("requests").insert({ project_id: projectId, kind, message });
  if (error) return { error: "Permintaan gagal terkirim. Coba lagi beberapa saat." };

  revalidatePath("/klien");
  return { ok: true };
}

