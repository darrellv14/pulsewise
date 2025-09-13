"use client";
import { useState } from "react";
import { api } from "../../lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "../../components/ui/card";
import { Input } from "../../components/ui/input";
import { Button } from "../../components/ui/button";

export default function ConsumptionPage() {
  const [diaryId, setDiaryId] = useState("");
  const [name, setName] = useState("");
  const [type, setType] = useState("Food");

  async function add() {
    if (!diaryId || !name) return;
    await api(`/lifestyle/consumptions?diary_id=${diaryId}`, {
      method: "POST",
      body: JSON.stringify({ type, name, occurred_at: new Date().toISOString() }),
    });
    setName("");
  }

  return (
    <main className="max-w-3xl mx-auto p-6">
      <Card>
        <CardHeader>
          <CardTitle>Consumption</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 sm:grid-cols-4 gap-2 items-end">
            <Input placeholder="Diary ID" value={diaryId} onChange={(e) => setDiaryId(e.target.value)} />
            <select className="border border-slate-300 rounded-lg h-10 px-3 text-sm" value={type} onChange={(e) => setType(e.target.value)}>
              <option>Food</option>
              <option>Drink</option>
            </select>
            <Input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
            <Button onClick={add}>Add</Button>
          </div>
        </CardContent>
      </Card>
    </main>
  );
}
