import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDuration(ms: number): string {
  if (ms < 1000) return `${Math.round(ms)} ms`;
  return `${(ms / 1000).toFixed(2)} s`;
}

export function friendlyApiError(payload: unknown): string | null {
  if (!payload || typeof payload !== "object") return null;
  const envelope = payload as {
    error?: { code?: string; message?: string; details?: unknown };
  };
  if (!envelope.error) return null;

  const { code, message, details } = envelope.error;
  const parts = [message || "Something went wrong with this request."];

  if (code) parts.unshift(`[${code}]`);

  if (Array.isArray(details)) {
    const fieldErrors = details
      .map((d) => {
        if (d && typeof d === "object") {
          const item = d as { loc?: unknown[]; msg?: string };
          const loc = Array.isArray(item.loc)
            ? item.loc.filter((x) => typeof x === "string").join(".")
            : "";
          return loc && item.msg ? `${loc}: ${item.msg}` : item.msg;
        }
        return typeof d === "string" ? d : null;
      })
      .filter(Boolean);
    if (fieldErrors.length) {
      parts.push(fieldErrors.join("; "));
    }
  } else if (details && typeof details === "object") {
    parts.push(JSON.stringify(details));
  } else if (typeof details === "string") {
    parts.push(details);
  }

  return parts.filter(Boolean).join(" — ");
}
