import { getSession } from "next-auth/react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "/api";

export async function api(path: string, init?: RequestInit) {
  const session = await getSession();
  const headers = new Headers(init?.headers);
  headers.set("Content-Type", "application/json");
  const token = (session as any)?.accessToken as string | undefined;
  if (token) headers.set("Authorization", `Bearer ${token}`);
  return fetch(`${API_BASE}${path}`, { ...init, headers });
}
