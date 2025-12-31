/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: { sans: ['Vazirmatn', 'sans-serif'] },
      colors: {
        navy: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          800: '#1e1b4b',
          900: '#0f172a',
          950: '#020617',
        },
        sky: { DEFAULT: '#38bdf8', 500: '#38bdf8', 600: '#0284c7' }
      },
    },
  },
  plugins: [],
}