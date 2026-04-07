import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatScore(score: number): string {
  return `${Math.round(score * 100)}%`;
}

export function scoreColor(score: number): string {
  if (score >= 0.8) return "#5fc992"; // green
  if (score >= 0.6) return "#ffbc33"; // yellow
  return "#FF6363"; // red
}

export function truncate(str: string, max: number): string {
  return str.length > max ? str.slice(0, max).trimEnd() + "…" : str;
}
