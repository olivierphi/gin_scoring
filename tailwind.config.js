
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/gin_scoring/apps/*/jinja2/**/*.html"],
  theme: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/typography"),
    require("@tailwindcss/forms"),
    require("@tailwindcss/aspect-ratio"),
    require("@tailwindcss/container-queries"),
    require("daisyui"),
  ],
  daisyui: {
    // https://daisyui.com/docs/config/
    themes: ["pastel", "night"],
    darkTheme: "night",
    logs: false,
  }
};
