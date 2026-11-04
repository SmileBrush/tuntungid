import { NextResponse } from "next/server";
import { createServerClient } from "@supabase/ssr";
import { guardPath, resolveRole } from "./lib/access.js";
import { hasSupabaseEnv } from "./lib/env.js";

export async function middleware(request) {
  if (!hasSupabaseEnv()) {
    return request.nextUrl.pathname === "/masuk"
      ? NextResponse.next()
      : NextResponse.redirect(new URL("/masuk", request.url));
  }

  let response = NextResponse.next({ request });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL,
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY,
    {
      cookies: {
        getAll: () => request.cookies.getAll(),
        setAll(list) {
          list.forEach(({ name, value }) => request.cookies.set(name, value));
          response = NextResponse.next({ request });
          list.forEach(({ name, value, options }) => response.cookies.set(name, value, options));
        }
      }
    }
  );

  const { data } = await supabase.auth.getUser();
  const role = resolveRole(data?.user);
  const target = guardPath(request.nextUrl.pathname, role);

  if (target) {
    const redirect = NextResponse.redirect(new URL(target, request.url));
    response.cookies.getAll().forEach((c) => redirect.cookies.set(c));
    return redirect;
  }
  return response;
}

export const config = {
  matcher: ["/admin/:path*", "/klien/:path*", "/masuk"]
};
