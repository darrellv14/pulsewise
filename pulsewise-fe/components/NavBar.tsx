"use client";
import Link from "next/link";
import { useSession, signOut } from "next-auth/react";
import {
  HeartPulse,
  BookOpenText,
  Pill,
  Salad,
  Dumbbell,
  GraduationCap,
  LogIn,
} from "lucide-react";

export default function NavBar() {
  const { data: session } = useSession();
  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200 bg-white/80 backdrop-blur supports-[backdrop-filter]:bg-white/60">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <HeartPulse className="text-sky-600" />
          <Link href="/" className="text-slate-800 font-semibold">
            PulseWise
          </Link>
        </div>
        <nav className="hidden md:flex items-center gap-6 text-sm text-slate-600">
          <Link
            href="/diaries"
            className="hover:text-slate-900 flex items-center gap-2"
          >
            <BookOpenText size={18} />
            Diaries
          </Link>
          <Link
            href="/meds"
            className="hover:text-slate-900 flex items-center gap-2"
          >
            <Pill size={18} />
            Meds
          </Link>
          <Link
            href="/consumption"
            className="hover:text-slate-900 flex items-center gap-2"
          >
            <Salad size={18} />
            Consumption
          </Link>
          <Link
            href="/activities"
            className="hover:text-slate-900 flex items-center gap-2"
          >
            <Dumbbell size={18} />
            Activities
          </Link>
          <Link
            href="/education"
            className="hover:text-slate-900 flex items-center gap-2"
          >
            <GraduationCap size={18} />
            Education
          </Link>
        </nav>
        <div className="flex items-center gap-3">
          {session ? (
            <>
              <span className="text-sm text-slate-600 hidden sm:inline">
                Hi, {session.user?.name}
              </span>
              <button
                onClick={() => signOut({ callbackUrl: "/" })}
                className="inline-flex items-center gap-2 rounded-lg border border-slate-300 px-3 py-2 text-sm hover:bg-slate-50 text-slate-700"
              >
                Sign out
              </button>
            </>
          ) : (
            <Link
              href="/auth/signin"
              className="inline-flex items-center gap-2 rounded-lg border border-slate-300 px-3 py-2 text-sm hover:bg-slate-50 text-slate-700"
            >
              <LogIn size={18} /> Sign in
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
