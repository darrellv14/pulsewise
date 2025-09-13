"use client";
import { SessionProvider as Provider } from "next-auth/react";
import * as React from "react";

export default function SessionProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  return <Provider>{children}</Provider>;
}
