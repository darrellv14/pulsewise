"use client";
import { useEffect, useState } from "react";
import { api } from "../../lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "../../components/ui/card";
import { Input } from "../../components/ui/input";
import { Button } from "../../components/ui/button";

export default function MedsPage() {
  const [userId, setUserId] = useState("");
  const [list, setList] = useState<any[]>([]);
  const [name, setName] = useState("");

  async function load() {
    if (!userId) return;
    const res = await api(`/meds?user_id=${userId}`);
    setList(await res.json());
  }

  async function create() {
    if (!userId || !name) return;
    await api(`/meds`, {
      method: "POST",
      body: JSON.stringify({ user_id: userId, name, active: true }),
    });
    setName("");
    load();
  }

  return (
    <main className="max-w-5xl mx-auto p-6">
      <Card>
        <CardHeader>
          <CardTitle>Medications</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 items-end">
            <Input placeholder="User ID" value={userId} onChange={(e) => setUserId(e.target.value)} />
            <Input placeholder="New medication name" value={name} onChange={(e) => setName(e.target.value)} />
            <div className="flex gap-2">
              <Button variant="outline" onClick={load}>Load</Button>
              <Button onClick={create}>Add</Button>
            </div>
          </div>
          <ul className="mt-4 space-y-2">
            {list.map((m) => (
              <li key={m.medication_id} className="rounded-lg border border-slate-200 p-3">
                <div className="font-medium text-slate-800">{m.name}</div>
                <div className="text-xs text-slate-500">{m.route || "—"} {m.dosage_amount ? `${m.dosage_amount} ${m.dosage_unit || ""}` : ""}</div>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </main>
  );
}
