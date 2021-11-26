module.exports = {
  purge: ["./templates/**/*.html"],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      spacing: {
        "25vh": "25vh",
        "50vh": "50vh",
        "65vh": "65vh",
        "75vh": "75vh",
        "85vh": "85vh",
        "90vh": "90vh",
      },
    },
  },
  variants: {
    extend: {
      brightness: ["hover", "focus"],
      fontWeight: ["hover", "focus"],
    },
  },
  plugins: [],
};
