/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'primary': '#e3e3db',
        'secondary': '#000000',
        'dark-primary': '#111827', /* 深蓝黑色而不是灰色 */
        'dark-secondary': '#e3e3db'
      },
      fontFamily: {
        'sans': ['Saans TRIAL', 'sans-serif'],
      },
      zIndex: {
        '100': '100',
      },
      typography: {
        DEFAULT: {
          css: {
            color: '#000000',
            a: {
              color: '#000000',
              '&:hover': {
                color: '#2c5282',
              },
            },
            'h1,h2,h3,h4,h5,h6': {
              color: '#000000',
              fontWeight: '600',
            },
          },
        },
        dark: {
          css: {
            color: '#e3e3db',
            a: {
              color: '#e3e3db',
              '&:hover': {
                color: '#90cdf4',
              },
            },
            'h1,h2,h3,h4,h5,h6': {
              color: '#e3e3db',
              fontWeight: '600',
            },
          },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}

