"use client";
import { useState } from "react";
import { signIn } from "next-auth/react";
import { Button } from "../../../components/ui/button";
import { Input } from "../../../components/ui/input";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "../../../components/ui/card";

export default function SignInPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSignIn() {
    setLoading(true);
    await signIn("credentials", {
      username,
      password,
      callbackUrl: "/diaries",
    });
    setLoading(false);
  }

  return (
    <main className="min-h-[80svh] grid place-items-center p-6">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-slate-800">Welcome back</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <Input
              placeholder="Username or email"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <Input
              placeholder="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button
              onClick={handleSignIn}
              disabled={loading}
              className="w-full"
            >
              {loading ? "Signing in..." : "Sign in"}
            </Button>
          </div>
        </CardContent>
      </Card>
    </main>
  );
}
