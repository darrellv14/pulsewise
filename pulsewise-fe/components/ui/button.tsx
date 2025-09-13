import * as React from "react";

type Variant = "default" | "outline" | "ghost" | "soft";
type Size = "sm" | "md" | "lg" | "icon";

function cls(...parts: Array<string | false | undefined>) {
  return parts.filter(Boolean).join(" ");
}

const base =
  "inline-flex items-center justify-center whitespace-nowrap rounded-lg text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-400 disabled:pointer-events-none disabled:opacity-50 gap-2";

const variantMap: Record<Variant, string> = {
  default: "bg-sky-600 text-white hover:bg-sky-500",
  outline: "border border-slate-300 bg-white text-slate-800 hover:bg-slate-50",
  ghost: "bg-transparent text-slate-700 hover:bg-slate-100",
  soft: "bg-sky-50 text-sky-700 hover:bg-sky-100 border border-sky-100",
};

const sizeMap: Record<Size, string> = {
  sm: "h-9 px-3",
  md: "h-10 px-4",
  lg: "h-11 px-5",
  icon: "h-10 w-10",
};

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className = "", variant = "default", size = "md", ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cls(base, variantMap[variant], sizeMap[size], className)}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";
