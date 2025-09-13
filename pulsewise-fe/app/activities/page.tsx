"use client";
import { useEffect, useState } from "react";
import { api } from "../../lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "../../components/ui/card";
import { Input } from "../../components/ui/input";
import { Button } from "../../components/ui/button";

export default function ActivitiesPage() {
  const [diaryId, setDiaryId] = useState("");
  const [list, setList] = useState<any[]>([]);
  const [name, setName] = useState("");
  const [duration, setDuration] = useState("");

  async function load() {
    if (!diaryId) return;
    const res = await api(`/lifestyle/activities?diary_id=${diaryId}`);
    setList(await res.json());
  }

  async function create() {
    if (!diaryId || !name || !duration) return;
    await api(`/lifestyle/activities?diary_id=${diaryId}`, {
      method: "POST",
      body: JSON.stringify({ name, duration_min: Number(duration), occurred_at: new Date().toISOString() }),
    });
    setName(""); setDuration("");
    load();
  }

  return (
    <main className="max-w-5xl mx-auto p-6">
      <Card>
        <CardHeader>
          <CardTitle>Activities</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 sm:grid-cols-4 gap-2 items-end">
            <Input placeholder="Diary ID" value={diaryId} onChange={(e) => setDiaryId(e.target.value)} />
            <Input placeholder="Activity name" value={name} onChange={(e) => setName(e.target.value)} />
            <Input placeholder="Duration (min)" value={duration} onChange={(e) => setDuration(e.target.value)} />
            <div className="flex gap-2">
              <Button variant="outline" onClick={load}>Load</Button>
              <Button onClick={create}>Add</Button>
            </div>
          </div>
          <ul className="mt-4 space-y-2">
            {list.map((m) => (
              <li key={m.activity_id} className="rounded-lg border border-slate-200 p-3">
                <div className="font-medium text-slate-800">{m.name}</div>
                <div className="text-xs text-slate-500">{m.duration_min} min</div>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </main>
  );
}
