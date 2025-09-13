"use client";
import { useEffect, useState } from "react";
import { api } from "../../lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "../../components/ui/card";

export default function EducationPage() {
  const [modules, setModules] = useState<any[]>([]);

  useEffect(() => {
    (async () => {
      const res = await api(`/edu/modules`);
      setModules(await res.json());
    })();
  }, []);

  return (
    <main className="max-w-5xl mx-auto p-6 grid gap-4">
      {modules.map((m) => (
        <Card key={m.module_id}>
          <CardHeader>
            <CardTitle>{m.title}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-slate-600 text-sm">{m.description}</p>
          </CardContent>
        </Card>
      ))}
    </main>
  );
}
