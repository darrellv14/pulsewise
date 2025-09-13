"use client";
import { useState, useMemo } from "react";
import {
  Search,
  Plus,
  BookUser,
  HeartPulse,
  MousePointer,
  LoaderCircle,
} from "lucide-react";
import KeyboardFocusKeeper from "../_components/KeyboardFocusKeeper";

type Diary = {
  diary_id: string;
  user_id: string;
  diary_date: string;
  notes?: string | null;
};

type Vital = {
  vital_id: string;
  measured_at: string;
  systolic?: number | null;
  diastolic?: number | null;
  heart_rate?: number | null;
  weight_kg?: number | null;
};

const API = (p: string) => `${process.env.NEXT_PUBLIC_API_BASE}${p}`;

export default function DiariesPage() {
  const [userId, setUserId] = useState("");
  const [date, setDate] = useState("");
  const [notes, setNotes] = useState("");
  const [list, setList] = useState<Diary[]>([]);
  const [selected, setSelected] = useState<Diary | null>(null);
  const [isLoadingDiaries, setIsLoadingDiaries] = useState(false);
  const [isLoadingVitals, setIsLoadingVitals] = useState(false);

  const [systolic, setSystolic] = useState("");
  const [diastolic, setDiastolic] = useState("");
  const [hr, setHr] = useState("");
  const [weight, setWeight] = useState("");
  const [vitals, setVitals] = useState<Vital[]>([]);

  async function loadDiaries(uid: string) {
    if (!uid) return;
    setIsLoadingDiaries(true);
    setSelected(null);
    setVitals([]);
    try {
      const res = await fetch(API(`/diaries?user_id=${uid}`), { cache: "no-store" });
      const data = await res.json();
      setList(data);
    } catch (error) {
      console.error("Failed to load diaries:", error);
      alert("Failed to load diaries.");
    } finally {
      setIsLoadingDiaries(false);
    }
  }

  async function createDiary() {
    if (!userId || !date) return alert("User ID & Date are required.");
    try {
      const res = await fetch(API(`/diaries`), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, diary_date: date, notes }),
      });
      if (!res.ok) { throw new Error(await res.text()); }
      setNotes("");
      await loadDiaries(userId);
    } catch (error) {
      console.error("Failed to create diary:", error);
      alert(`Failed to create diary: ${error}`);
    }
  }

  async function selectDiary(d: Diary) {
    setSelected(d);
    setIsLoadingVitals(true);
    try {
      const res = await fetch(API(`/diaries/${d.diary_id}/vitals`));
      setVitals(await res.json());
    } catch (error) {
      console.error("Failed to load vitals:", error);
      alert("Failed to load vitals.");
    } finally {
      setIsLoadingVitals(false);
    }
  }

  async function addVital() {
    if (!selected) return;
    try {
      const res = await fetch(API(`/diaries/${selected.diary_id}/vitals`), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          measured_at: new Date().toISOString(),
          systolic: systolic ? Number(systolic) : undefined,
          diastolic: diastolic ? Number(diastolic) : undefined,
          heart_rate: hr ? Number(hr) : undefined,
          weight_kg: weight ? Number(weight) : undefined,
        }),
      });
      if (!res.ok) { throw new Error(await res.text()); }
      await selectDiary(selected);
      setSystolic(""); setDiastolic(""); setHr(""); setWeight("");
    } catch (error) {
      console.error("Failed to add vital:", error);
      alert(`Failed to add vital: ${error}`);
    }
  }
  
  const sortedVitals = useMemo(() => {
    return [...vitals].sort((a, b) => new Date(b.measured_at).getTime() - new Date(a.measured_at).getTime());
  }, [vitals]);

  const Card = ({ children, className = '' }: { children: React.ReactNode, className?: string }) => (
    <div className={`bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 ${className}`}>
      {children}
    </div>
  );
  
  const inputCls = "w-full bg-slate-700/50 border border-slate-600 rounded-lg px-3 py-2 text-sm text-slate-200 placeholder-slate-400 outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition";
  const btn = "flex items-center justify-center gap-2 rounded-lg px-4 py-2 text-sm font-semibold transition disabled:opacity-50 disabled:cursor-not-allowed";
  const btnPrimary = `${btn} bg-indigo-600 text-white hover:bg-indigo-500 active:scale-[.98]`;
  const btnGhost = `${btn} bg-slate-700/50 border border-slate-600 text-slate-200 hover:bg-slate-700`;

  return (
    <main className="bg-slate-900 text-slate-100 min-h-[100svh] overscroll-contain font-sans p-4 sm:p-6 lg:p-8">
      <KeyboardFocusKeeper />
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold tracking-tight">PulseWise Diaries</h1>
        
        <Card className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 items-end">
            <input
              className={inputCls}
              placeholder="User ID (UUID)"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              autoComplete="off"
              autoCorrect="off"
              autoCapitalize="off"
              inputMode="text"
            />
            <input
              className={inputCls}
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              autoComplete="off"
            />
            <input
              className={inputCls + " md:col-span-2 lg:col-span-1"}
              placeholder="Notes (optional)"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              autoComplete="off"
              autoCorrect="off"
              autoCapitalize="off"
            />
            <div className="flex gap-2 w-full lg:col-span-2">
              <button type="button" className={`${btnGhost} w-full`} onClick={() => loadDiaries(userId)} disabled={!userId || isLoadingDiaries}>
                {isLoadingDiaries ? <LoaderCircle className="animate-spin" size={18} /> : <Search size={18} />} Load
              </button>
              <button type="button" className={`${btnPrimary} w-full`} onClick={createDiary}>
                <Plus size={18} /> Create
              </button>
            </div>
          </div>
        </Card>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
          <Card>
            <h2 className="flex items-center gap-3 text-xl font-semibold">
              <BookUser className="text-indigo-400" />
              <span>User Diaries</span>
            </h2>
            <ul className="mt-4 space-y-3 h-[60vh] overflow-y-auto pr-2">
              {isLoadingDiaries ? (
                <div className="flex items-center justify-center h-full text-slate-400">
                  <LoaderCircle className="animate-spin mr-2" /> Loading diaries...
                </div>
              ) : list.length > 0 ? (
                list.map((d) => (
                  <li
                    key={d.diary_id}
                    onClick={() => selectDiary(d)}
                    className={`cursor-pointer rounded-lg border-2 p-4 transition-all duration-200 ${
                      selected?.diary_id === d.diary_id
                        ? "bg-indigo-500/20 border-indigo-500"
                        : "border-slate-700 hover:border-slate-500 hover:bg-slate-800"
                    }`}
                  >
                    <div className="font-medium text-slate-100">{new Date(d.diary_date + 'T00:00:00').toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</div>
                    <div className="text-xs text-slate-400 mt-1">{d.notes || "No notes"}</div>
                  </li>
                ))
              ) : (
                <div className="text-center text-slate-500 pt-16">Enter a User ID and click 'Load' to see diaries.</div>
              )}
            </ul>
          </Card>
          
          <Card>
            <h2 className="flex items-center gap-3 text-xl font-semibold">
              <HeartPulse className="text-red-400" />
              <span>Vital Signs {selected ? `for ${new Date(selected.diary_date + 'T00:00:00').toLocaleDateString()}` : ""}</span>
            </h2>
            {selected ? (
              <>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-4">
                  <input
                    className={inputCls}
                    type="text"
                    inputMode="numeric"
                    pattern="[0-9]*"
                    placeholder="SYS (mmHg)"
                    value={systolic}
                    onChange={(e) => setSystolic(e.target.value)}
                    autoComplete="off"
                  />
                  <input
                    className={inputCls}
                    type="text"
                    inputMode="numeric"
                    pattern="[0-9]*"
                    placeholder="DIA (mmHg)"
                    value={diastolic}
                    onChange={(e) => setDiastolic(e.target.value)}
                    autoComplete="off"
                  />
                  <input
                    className={inputCls}
                    type="text"
                    inputMode="numeric"
                    pattern="[0-9]*"
                    placeholder="HR (bpm)"
                    value={hr}
                    onChange={(e) => setHr(e.target.value)}
                    autoComplete="off"
                  />
                  <input
                    className={inputCls}
                    type="text"
                    inputMode="decimal"
                    placeholder="Weight (kg)"
                    value={weight}
                    onChange={(e) => setWeight(e.target.value)}
                    autoComplete="off"
                  />
                </div>
                <button type="button" className={btnPrimary + " mt-3 w-full"} onClick={addVital}>
                  <Plus size={18}/> Add Vital Reading
                </button>

                <div className="mt-4 h-[45vh] overflow-y-auto">
                  {isLoadingVitals ? (
                    <div className="flex items-center justify-center h-full text-slate-400">
                      <LoaderCircle className="animate-spin mr-2" /> Loading vitals...
                    </div>
                  ) : (
                    <div className="border border-slate-700 rounded-lg overflow-hidden">
                      <table className="w-full text-sm text-left">
                        <thead className="bg-slate-700/50 text-xs text-slate-300 uppercase tracking-wider">
                          <tr>
                            <th scope="col" className="px-4 py-3">Time</th>
                            <th scope="col" className="px-4 py-3 text-center">SYS</th>
                            <th scope="col" className="px-4 py-3 text-center">DIA</th>
                            <th scope="col" className="px-4 py-3 text-center">HR</th>
                            <th scope="col" className="px-4 py-3 text-center">W(kg)</th>
                          </tr>
                        </thead>
                        <tbody>
                          {sortedVitals.map((v) => (
                            <tr key={v.vital_id} className="bg-slate-800 border-b border-slate-700 hover:bg-slate-700/50">
                              <td className="px-4 py-3 font-medium">{new Date(v.measured_at).toLocaleTimeString()}</td>
                              <td className="px-4 py-3 text-center">{v.systolic ?? "-"}</td>
                              <td className="px-4 py-3 text-center">{v.diastolic ?? "-"}</td>
                              <td className="px-4 py-3 text-center">{v.heart_rate ?? "-"}</td>
                              <td className="px-4 py-3 text-center">{v.weight_kg ?? "-"}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              </>
            ) : (
              <div className="flex flex-col items-center justify-center h-full text-slate-500 text-center">
                <MousePointer size={48} className="mb-4" />
                <p className="font-semibold">Select a diary</p>
                <p className="text-sm">Choose an entry from the left to view and add vital signs.</p>
              </div>
            )}
          </Card>
        </div>
      </div>
    </main>
  );
}
