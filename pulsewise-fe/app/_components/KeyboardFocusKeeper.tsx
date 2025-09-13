"use client";
import { useEffect, useRef } from "react";

export default function KeyboardFocusKeeper() {
  const lastFocus = useRef<HTMLElement | null>(null);

  useEffect(() => {
    const onFocus = (e: Event) => {
      const t = e.target as HTMLElement | null;
      if (!t) return;
      const tag = t.tagName;
      const editable = (t as HTMLElement).isContentEditable;
      if (tag === "INPUT" || tag === "TEXTAREA" || editable) {
        lastFocus.current = t;
      }
    };

    const vv = (window as any).visualViewport as VisualViewport | undefined;
    const onResize = () => {
      // Refocus kalau tiba-tiba body yang aktif (fokus hilang saat keyboard muncul)
      window.requestAnimationFrame(() => {
        if (document.activeElement === document.body && lastFocus.current) {
          (lastFocus.current as any).focus?.({ preventScroll: true });
        }
      });
    };

    document.addEventListener("focusin", onFocus, true);
    if (vv) vv.addEventListener("resize", onResize);
    else window.addEventListener("resize", onResize);

    return () => {
      document.removeEventListener("focusin", onFocus, true);
      if (vv) vv.removeEventListener("resize", onResize);
      else window.removeEventListener("resize", onResize);
    };
  }, []);

  return null;
}
