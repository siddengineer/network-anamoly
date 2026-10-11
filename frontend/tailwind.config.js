/** @type {import("tailwindcss").Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        soc: {
          bg: "#080c17",
          card: "#0f172a",
          cardLight: "#162036",
          border: "#1e293b",
          borderLight: "#334155",
          accent: "#06b6d4",
          normal: "#10b981",
          warning: "#f59e0b",
          danger: "#ef4444",
          muted: "#94a3b8"
        }
      }
    },
  },
  plugins: [],
}
