module.exports = {
  purge: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}'
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      flex: {
        '3': '3 3 0%'
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}