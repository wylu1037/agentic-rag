import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        /* ── Raycast Core ────────────────────────────────── */
        rc: {
          bg:       "#07080a",
          surface:  "#101111",
          elevated: "#1b1c1e",
          "key-s":  "#121212",
          "key-e":  "#0d0d0d",
          /* text */
          white:   "#f9f9f9",
          lt:      "#cecece",
          silver:  "#c0c0c0",
          mid:     "#9c9c9d",
          dim:     "#6a6b6c",
          dark:    "#434345",
          /* accent */
          red:    "#FF6363",
          blue:   "hsl(202,100%,67%)",
          green:  "hsl(151,59%,59%)",
          yellow: "hsl(43,100%,60%)",
        },
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
        mono: ["GeistMono", "ui-monospace", "SFMono-Regular", "Menlo", "monospace"],
      },
      letterSpacing: {
        "rc-body": "0.2px",
        "rc-wide": "0.3px",
        "rc-btn":  "0.3px",
      },
      borderRadius: {
        pill:  "86px",
        card:  "12px",
        "card-lg": "16px",
        btn:   "6px",
        input: "8px",
      },
      boxShadow: {
        /* double-ring card */
        card: "rgb(27,28,30) 0px 0px 0px 1px, rgb(7,8,10) 0px 0px 0px 1px inset",
        /* button mac-style */
        btn:  "rgba(255,255,255,0.05) 0px 1px 0px 0px inset, rgba(255,255,255,0.25) 0px 0px 0px 1px, rgba(0,0,0,0.2) 0px -1px 0px 0px inset",
        /* pill cta */
        pill: "rgba(255,255,255,0.1) 0px 1px 0px 0px inset",
        /* elevated floating panel */
        floating: "rgba(0,0,0,0.5) 0px 0px 0px 2px, rgba(255,255,255,0.19) 0px 0px 14px",
      },
      animation: {
        "pulse-dot":   "pulse-dot 1.4s ease-in-out infinite",
        "shimmer":     "shimmer 1.5s linear infinite",
        "fade-up":     "fade-up 0.35s cubic-bezier(0.16,1,0.3,1) forwards",
      },
      keyframes: {
        "pulse-dot": {
          "0%,80%,100%": { opacity: "0.3", transform: "scale(0.8)" },
          "40%":         { opacity: "1",   transform: "scale(1)" },
        },
        "shimmer": {
          "0%":   { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
        "fade-up": {
          "0%":   { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
