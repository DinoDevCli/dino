/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./lib/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "var(--ink)",
        surface: "var(--surface)",
        text: "var(--text)",
        "text-muted": "var(--text-muted)",
        seal: "var(--seal)",
        "seal-hover": "var(--seal-hover)",
        drift: "var(--drift)",
        aligned: "var(--aligned)",
        border: "var(--border)",
        background: "var(--ink)",
        foreground: "var(--text)",
        muted: "var(--text-muted)",
        accent: "var(--seal)",
      },
      maxWidth: {
        content: "40rem",
        page: "64rem",
        narrow: "40rem",
      },
      fontFamily: {
        display: ["var(--font-display)", "ui-serif", "Georgia", "serif"],
        body: ["var(--font-body)", "ui-sans-serif", "system-ui", "sans-serif"],
        sans: ["var(--font-body)", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["var(--font-mono)", "ui-monospace", "monospace"],
      },
      spacing: {
        section: "6rem",
        gutter: "1.5rem",
      },
    },
  },
  plugins: [],
};
