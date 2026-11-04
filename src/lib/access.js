export function resolveRole(user) {
  if (!user) return "anonymous";
  return user.app_metadata?.role === "admin" ? "admin" : "client";
}

export function homePathFor(role) {
  if (role === "admin") return "/admin";
  if (role === "client") return "/klien";
  return "/masuk";
}

// Mengembalikan path tujuan pengalihan, atau null bila akses diizinkan.
export function guardPath(pathname, role) {
  if (pathname.startsWith("/admin")) {
    if (role === "admin") return null;
    return role === "client" ? "/klien" : "/masuk";
  }
  if (pathname.startsWith("/klien")) {
    if (role === "client") return null;
    return role === "admin" ? "/admin" : "/masuk";
  }
  if (pathname === "/masuk" && role !== "anonymous") return homePathFor(role);
  return null;
}

