"use client";
import { useEffect, useState } from "react";
import { Wifi, WifiOff, LoaderCircle } from "lucide-react";
import KeyboardFocusKeeper from "../_components/KeyboardFocusKeeper";

type StatusState = "loading" | "success" | "error";

export default function PingPage() {
  const [status, setStatus] = useState<StatusState>("loading");
  const [message, setMessage] = useState("Pinging backend...");

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_BASE}/health`)
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP error! status: ${r.status}`);
        return r.json();
      })
      .then((j) => {
        setStatus("success");
        setMessage(JSON.stringify(j, null, 2));
      })
      .catch((e) => {
        setStatus("error");
        setMessage("ERR: " + e.message);
      });
  }, []);

  const statusInfo = {
    loading: {
      icon: <LoaderCircle className="animate-spin h-8 w-8 text-slate-400" />,
      text: "Pinging...",
      textColor: "text-slate-400",
      bgColor: "bg-slate-700/50",
    },
    success: {
      icon: <Wifi className="h-8 w-8 text-green-400" />,
      text: "Connection Successful",
      textColor: "text-green-400",
      bgColor: "bg-green-500/10",
    },
    error: {
      icon: <WifiOff className="h-8 w-8 text-red-400" />,
      text: "Connection Failed",
      textColor: "text-red-400",
      bgColor: "bg-red-500/10",
    },
  } as const;

  const currentStatus = statusInfo[status];

  return (
    <main className="font-sans bg-slate-900 text-slate-200 flex items-center justify-center min-h-[100svh] overscroll-contain p-4">
      <KeyboardFocusKeeper />
      <div className="w-full max-w-2xl bg-slate-800/50 border border-slate-700 rounded-2xl shadow-2xl p-8 backdrop-blur-sm">
        <div className="flex items-center gap-4">
          {currentStatus.icon}
          <div>
            <h1 className={`text-2xl font-bold ${currentStatus.textColor}`}>
              {currentStatus.text}
            </h1>
            <p className="text-sm text-slate-400 mt-1">FE → BE Ping Status</p>
          </div>
        </div>
        <div className="mt-6">
          <p className="text-xs text-slate-500 font-mono">
            API_BASE: {process.env.NEXT_PUBLIC_API_BASE}
          </p>
          <pre className={`mt-2 rounded-lg p-4 text-sm font-mono whitespace-pre-wrap break-all ${currentStatus.bgColor} text-slate-300`}>
            {message}
          </pre>
        </div>
      </div>
    </main>
  );
}
