"use client";

import { useState } from "react";
import { api } from "@/lib/api";

export default function ECGPage() {
  const [signalText, setSignalText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const submit = async () => {
    setError(null);
    setResult(null);
    setLoading(true);
    try {
      const values = signalText
        .split(/[\s,]+/)
        .filter(Boolean)
        .map((v) => Number(v));
      const res = await api("/ecg/predict", {
        method: "POST",
        body: JSON.stringify({ signal: values, norm: "zscore" }),
      });
      if (!res.ok) {
        const t = await res.text();
        throw new Error(t);
      }
      const data = await res.json();
      setResult(data);
    } catch (e: any) {
      setError(e.message || String(e));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-4">
      <h1 className="text-2xl font-semibold">ECG Prediction</h1>
      <p className="text-sm text-gray-600">
        Paste {process.env.NEXT_PUBLIC_ECG_LENGTH || 187} comma/space separated numbers
        representing one ECG signal sample.
      </p>
      <textarea
        className="w-full border rounded p-2 h-48"
        placeholder="0.12, 0.15, ..."
        value={signalText}
        onChange={(e) => setSignalText(e.target.value)}
      />
      <button
        onClick={submit}
        disabled={loading}
        className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
      >
        {loading ? "Predicting..." : "Predict"}
      </button>
      {error && <pre className="text-red-600 whitespace-pre-wrap">{error}</pre>}
      {result && (
        <div className="border rounded p-3">
          <div>Predicted Class: <b>{result.predicted_class}</b></div>
          <div>Probabilities: {result.probs.map((p: number) => p.toFixed(4)).join(", ")}</div>
        </div>
      )}
    </div>
  );
}
