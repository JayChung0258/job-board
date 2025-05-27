/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  safelist: [
    "max-h-[1000px]",
    "max-h-0",
    "opacity-0",
    "opacity-100",
    "translate-y-0",
    "-translate-y-4",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
