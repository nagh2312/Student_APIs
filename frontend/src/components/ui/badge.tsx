import { cn } from "@/lib/utils";
import type { HTMLAttributes } from "react";

type BadgeTone =
  | "neutral"
  | "success"
  | "warning"
  | "danger"
  | "info"
  | "accent";

const tones: Record<BadgeTone, string> = {
  neutral: "bg-surface text-muted-foreground border-border",
  success: "bg-[color-mix(in_srgb,var(--success)_12%,white)] text-success border-[color-mix(in_srgb,var(--success)_28%,white)]",
  warning: "bg-[color-mix(in_srgb,var(--warning)_14%,white)] text-[#92400e] border-[color-mix(in_srgb,var(--warning)_30%,white)]",
  danger: "bg-[color-mix(in_srgb,var(--danger)_12%,white)] text-danger border-[color-mix(in_srgb,var(--danger)_28%,white)]",
  info: "bg-primary-soft text-primary border-[color-mix(in_srgb,var(--primary)_25%,white)]",
  accent: "bg-accent-soft text-accent border-[color-mix(in_srgb,var(--accent)_25%,white)]",
};

export function Badge({
  className,
  tone = "neutral",
  ...props
}: HTMLAttributes<HTMLSpanElement> & { tone?: BadgeTone }) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium tracking-wide",
        tones[tone],
        className,
      )}
      {...props}
    />
  );
}
