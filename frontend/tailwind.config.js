/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Custom Theme Colors mapped to CSS variables in main.css
        primary: {
          DEFAULT: 'var(--color-primary)',
          50: '#fef2f5',
          100: '#fde6eb',
          200: '#fccdd6',
          300: '#f9a4b3',
          400: '#f4728f',
          500: 'var(--color-primary)',
          600: '#e0085a',
          700: '#c0074c',
          800: '#a0063e',
          900: '#800530'
        },
        secondary: {
          DEFAULT: 'var(--color-secondary)',
          dark: '#200f27',
          50: '#faf5ff',
          100: '#f3e8ff',
          200: '#e9d5ff',
          300: '#d8b4fe',
          400: '#c084fc',
          500: 'var(--color-secondary)',
          600: '#d1b5e0',
          700: '#ba93d1',
          800: '#a371c2',
          900: '#8c4fb3'
        },
        accent: {
          DEFAULT: 'var(--color-accent)',
          dark: '#4e2d5c',
          50: '#faf5ff',
          100: '#f3e8ff',
          200: '#e9d5ff',
          300: '#d8b4fe',
          400: '#c084fc',
          500: 'var(--color-accent)',
          600: '#b08cc0',
          700: '#9c75ae',
          800: '#885e9c',
          900: '#74478a'
        },
        background: {
          DEFAULT: 'var(--color-background)',
          dark: '#05041a',
          50: '#f8f7ff',
          100: '#f1f0ff',
          200: 'var(--color-background)',
          300: '#d1d0f0',
          400: '#bcbbe5',
          500: '#a7a6da',
          600: '#9291cf',
          700: '#7d7cc4',
          800: '#6867b9',
          900: '#5352ae'
        },
        text: {
          DEFAULT: 'var(--color-text)',
          dark: '#e1e0e0',
          50: '#f8f8f8',
          100: '#f1f1f1',
          200: '#e4e4e4',
          300: '#d7d7d7',
          400: '#cacaca',
          500: '#bdbdbd',
          600: '#b0b0b0',
          700: '#a3a3a3',
          800: '#969696',
          900: '#898989'
        },
        // Card and Component Colors
        'card-bg': 'var(--color-card-bg)',
        'card-border': 'var(--color-card-border)',
        'input-bg': 'var(--color-input-bg)',
        'input-border': 'var(--color-input-border)',
        // Success/Error Colors
        success: {
          DEFAULT: 'var(--color-success)',
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac',
          400: '#4ade80',
          500: 'var(--color-success)',
          600: '#16a34a',
          700: '#15803d',
          800: '#166534',
          900: '#14532d'
        },
        error: {
          DEFAULT: 'var(--color-error)',
          50: '#fef2f2',
          100: '#fee2e2',
          200: '#fecaca',
          300: '#fca5a5',
          400: '#f87171',
          500: 'var(--color-error)',
          600: '#dc2626',
          700: '#b91c1c',
          800: '#991b1b',
          900: '#7f1d1d'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace']
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem'
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'bounce-slow': 'bounce 2s infinite'
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        }
      }
    },
  },
  plugins: []
}