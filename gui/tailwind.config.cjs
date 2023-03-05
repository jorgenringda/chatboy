/** @type {import('tailwindcss').Config} */

const disabledCss = {
  "code::before": false,
  "code::after": false,
  pre: false,
  code: false,
  "pre code": false,
};

module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,html}",
    "./pages/**/*.{js,ts,jsx,tsx,html}",
    "./components/**/*.{js,ts,jsx,tsx,html}",
    "./public/index.html",
  ],
  theme: {
    extend: {
      typography: {
        DEFAULT: { css: disabledCss },
        sm: { css: disabledCss },
        lg: { css: disabledCss },
        xl: { css: disabledCss },
        "2xl": { css: disabledCss },
      },
    },
    fontFamily: {
      sans: ["Roboto", "sans-serif"],
      heading: ["Poppins", "sans-serif"],
    },
  },
  plugins: [require("tailwind-scrollbar"), require("@tailwindcss/typography")],
};
