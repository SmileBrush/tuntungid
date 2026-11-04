"use server";

import { redirect } from "next/navigation";
import { createSupabaseServer } from "../lib/supabase/server.js";
import { homePathFor, resolveRole } from "../lib/access.js";
import { hasSupabaseEnv } from "../lib/env.js";

export async function loginAction(_prev, formData) {
  const email = String(formData.get("email") || "").trim();
  const password = String(formData.get("password") || "");
  if (!email || !password) {
    return { error: "Isi email dan kata sandi." };
  }

  if (!hasSupabaseEnv()) {
    return { error: "Koneksi database belum diatur. Isi NEXT_PUBLIC_SUPABASE_URL dan NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY di .env.local, lalu mulai ulang server." };
  }

  const supabase = await createSupabaseServer();
  const { data, error } = await supabase.auth.signInWithPassword({ email, password });
  if (error || !data?.user) {
    return { error: "Email atau kata sandi salah. Periksa lagi, atau minta admin Tuntung.id mengatur ulang akun Anda." };
  }
  redirect(homePathFor(resolveRole(data.user)));
}

export async function logoutAction() {
  const supabase = await createSupabaseServer();
  await supabase.auth.signOut();
  redirect("/masuk");
}
