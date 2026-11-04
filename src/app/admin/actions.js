"use server";

import { revalidatePath } from "next/cache";
import { createSupabaseAdmin, getSessionUser } from "../../lib/supabase/server.js";
import { resolveRole } from "../../lib/access.js";
import { normalizeStage } from "../../lib/stages.js";

async function requireAdmin() {
  const { supabase, user } = await getSessionUser();
  if (resolveRole(user) !== "admin") return null;
  return supabase;
}

export async function createClientAction(_prev, formData) {
  const supabase = await requireAdmin();
  if (!supabase) return { error: "Hanya admin yang bisa membuat akun klien." };

  const email = String(formData.get("email") || "").trim();
  const fullName = String(formData.get("full_name") || "").trim();
  const company = String(formData.get("company") || "").trim();
  const password = String(formData.get("password") || "");
  const title = String(formData.get("title") || "").trim();
  if (!email || !fullName) return { error: "Isi nama dan email klien." };
  if (password.length < 8) return { error: "Kata sandi sementara minimal 8 karakter." };
  if (title.length < 3) return { error: "Isi nama proyek pertama klien." };

  let created;
  try {
    const admin = createSupabaseAdmin();
    const res = await admin.auth.admin.createUser({
      email,
      password,
      email_confirm: true,
      user_metadata: { full_name: fullName }
    });
    if (res.error) {
      return { error: `Akun gagal dibuat: ${res.error.message}` };
    }
    created = res.data.user;
  } catch (err) {
    return { error: err.message };
  }

  const profile = await supabase.from("profiles").insert({ id: created.id, full_name: fullName, company });
  if (profile.error) return { error: "Akun dibuat, tetapi profil gagal disimpan. Jalankan supabase/schema.sql lalu coba lagi." };

  const project = await supabase.from("projects").insert({ title, client_id: created.id });
  if (project.error) return { error: "Akun dibuat, tetapi proyek gagal disimpan. Tambahkan proyeknya lewat tab Proyek." };

  revalidatePath("/admin");
  return { ok: true, message: `Akun ${email} siap. Kirim kata sandi sementara ke klien lewat WhatsApp.` };
}

export async function updateStageAction(formData) {
  const supabase = await requireAdmin();
  if (!supabase) return;
  const id = String(formData.get("project_id") || "");
  await supabase.from("projects").update({ stage: normalizeStage(formData.get("stage")) }).eq("id", id);
  revalidatePath("/admin");
}

export async function updateScheduleAction(formData) {
  const supabase = await requireAdmin();
  if (!supabase) return;
  const id = String(formData.get("project_id") || "");
  await supabase
    .from("projects")
    .update({
      start_date: String(formData.get("start_date") || "") || null,
      target_date: String(formData.get("target_date") || "") || null
    })
    .eq("id", id);
  revalidatePath("/admin");
}

export async function addFileAction(formData) {
  const supabase = await requireAdmin();
  if (!supabase) return;
  const label = String(formData.get("label") || "").trim();
  const url = String(formData.get("url") || "").trim();
  if (!label || !/^https?:\/\//.test(url)) return;
  await supabase.from("project_files").insert({ project_id: String(formData.get("project_id") || ""), label, url });
  revalidatePath("/admin");
}

export async function replyRequestAction(formData) {
  const supabase = await requireAdmin();
  if (!supabase) return;
  const status = String(formData.get("status") || "diproses");
  if (!["baru", "diproses", "selesai"].includes(status)) return;
  await supabase
    .from("requests")
    .update({ status, admin_reply: String(formData.get("admin_reply") || "").trim() || null })
    .eq("id", String(formData.get("request_id") || ""));
  revalidatePath("/admin");
}

