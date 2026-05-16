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
        civic: {
          ink: "#172033",
          muted: "#526070",
          line: "#d8e0e8",
          paper: "#f7f9fb",
          blue: "#1f5f9d",
          teal: "#0f766e",
          gold: "#b7791f",
          red: "#b42318",
        },
      },
      boxShadow: {
        soft: "0 18px 45px rgba(23, 32, 51, 0.08)",
      },
    },
  },
  plugins: [],
};

export default config;
