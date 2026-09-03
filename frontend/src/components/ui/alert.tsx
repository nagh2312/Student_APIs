import { cn } from "@/lib/utils";
import type { HTMLAttributes } from "react";

type AlertTone = "info" | "success" | "warning" | "danger";

const tones: Record<AlertTone, string> = {
  info: "border-primary/25 bg-primary-soft text-foreground",
  success: "border-success/30 bg-[color-mix(in_srgb,var(--success)_10%,white)] text-foreground",
  warning: "border-warning/35 bg-[color-mix(in_srgb,var(--warning)_12%,white)] text-foreground",
  danger: "border-danger/30 bg-[color-mix(in_srgb,var(--danger)_10%,white)] text-foreground",
};

export function Alert({
  className,
  tone = "info",
  title,
  children,
  ...props
}: HTMLAttributes<HTMLDivElement> & {
  tone?: AlertTone;
  title?: string;
}) {
  return (
    <div
      role="alert"
      className={cn(
        "rounded-xl border px-4 py-3 text-sm leading-relaxed",
        tones[tone],
        className,
      )}
      {...props}
    >
      {title ? <p className="mb-1 font-medium">{title}</p> : null}
      <div className="text-muted-foreground [&_strong]:text-foreground">
        {children}
      </div>
    </div>
  );
}
