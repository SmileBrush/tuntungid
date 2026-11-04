"use server";

import { revalidatePath } from "next/cache";
import { getSessionUser } from "../../lib/supabase/server.js";
import { resolveRole } from "../../lib/access.js";
import { normalizeRating, canReviewProject } from "../../lib/stages.js";

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

export async function submitReviewAction(_prev, formData) {
  const { supabase, user } = await getSessionUser();
  if (resolveRole(user) !== "client") return { error: "Sesi berakhir. Masuk lagi untuk mengirim review." };

  const projectId = String(formData.get("project_id") || "");
  const rating = normalizeRating(formData.get("rating"));
  const feedback = String(formData.get("feedback") || "").trim();

  if (feedback.length < 5) return { error: "Tulis ulasan review minimal 5 karakter." };

  // Verifikasi proyek milik klien dan sudah di Tahap 5
  const { data: project, error: projError } = await supabase
    .from("projects")
    .select("stage")
    .eq("id", projectId)
    .maybeSingle();

  if (projError || !project) {
    return { error: "Data proyek tidak ditemukan." };
  }

  if (!canReviewProject(project.stage)) {
    return { error: "Review hanya dapat dikirimkan jika proyek telah mencapai Tahap 5 (Serah Terima & Garansi)." };
  }

  const { error: upsertError } = await supabase.from("reviews").upsert(
    {
      project_id: projectId,
      client_id: user.id,
      rating,
      feedback,
      is_published: false,
      updated_at: new Date().toISOString()
    },
    { onConflict: "project_id" }
  );

  if (upsertError) {
    return { error: `Gagal menyimpan review: ${upsertError.message || "Pastikan tabel reviews sudah dibuat di Supabase."}` };
  }

  revalidatePath("/klien");
  return { ok: true, message: "Terima kasih! Ulasan Anda berhasil disimpan dan akan ditinjau Admin." };
}


