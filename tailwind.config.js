/**
 * Compiled once with the standalone Tailwind CLI (no Node/npm needed) into
 * app/static/css/tailwind.css. Re-run after adding/removing utility classes
 * in any template:
 *
 *   ./tailwindcss.exe -i tailwind-input.css -o app/static/css/tailwind.css --minify
 *
 * (or python build_tailwind.py, which wraps the same command)
 */
module.exports = {
  content: ["./app/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        ink:    "#243B30",
        ink2:   "#365246",
        accent: "#B75A43",
        warm:   "#D29A31",
        mist:   "#F4EEDC",
        slate2: "#66756F",
        line:   "#D8CFB8",
        panel:  "#FFFDF7",
        sand:   "#EADDBD",
      },
      fontFamily: {
        display: ["Space Grotesk", "system-ui", "sans-serif"],
        body:    ["Manrope", "system-ui", "sans-serif"],
      },
      // The templates use bare numeric weights (font-700, font-600, font-500)
      // rather than Tailwind's named scale (font-bold, etc). Add them.
      fontWeight: {
        400: "400",
        500: "500",
        600: "600",
        700: "700",
      },
      boxShadow: {
        soft: "0 1px 2px rgba(20,34,53,.04), 0 16px 36px rgba(20,34,53,.08)",
        lift: "0 24px 60px rgba(20,34,53,.16)",
      },
    },
  },
  plugins: [],
};
