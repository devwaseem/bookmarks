/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */
const defaultTheme = require('tailwindcss/defaultTheme');
module.exports = {
    content: ['!./node_modules/', './**/*.html', './**/*.js', './**/*.ts', './**/*.py'],
    theme: {
        extend: {
            fontFamily: {
                sans: ['IBM Plex Sans', ...defaultTheme.fontFamily.sans],
                'serif-text': [...defaultTheme.fontFamily.serif],
                'serif-display': [...defaultTheme.fontFamily.serif],
                mono: [...defaultTheme.fontFamily.mono],
            },
            colors: {
                primary: {
                    DEFAULT: '#6c5be5',
                    50: '#f4f2ff',
                    100: '#eae8ff',
                    200: '#d8d4ff',
                    300: '#bab2ff',
                    400: '#9e8dff',
                    500: '#7755fd',
                    600: '#6632f5',
                    700: '#5720e1',
                    800: '#491abd',
                    900: '#3e189a',
                },
            },
            keyframes: {
                shake: {
                    '10%, 90%': {
                        transform: 'translate3d(-1px, 0, 0)',
                    },
                    '20%, 80%': {
                        transform: 'translate3d(2px, 0, 0)',
                    },
                    '30%, 50%, 70%': {
                        transform: 'translate3d(-4px, 0, 0)',
                    },
                    '40%, 60%': {
                        transform: 'translate3d(4px, 0, 0)',
                    },
                },
                wiggle: {
                    '0%, 100%': { transform: 'rotate(-3deg)' },
                    '50%': { transform: 'rotate(3deg)' },
                },
                indeterminate: {
                    '0%': {
                        left: '-35%',
                        right: '100%',
                    },
                    '60%': {
                        left: '100%',
                        right: '-90%',
                    },
                    '100%': {
                        left: '100%',
                        right: '-90%',
                    },
                },
            },
            animation: {
                indeterminate: 'indeterminate 2s cubic-bezier(0.65, 0.815, 0.735, 0.395) infinite',
            },
        },
    },
    daisyui: {
        themes: ['light'],
    },

    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('daisyui'),
    ],
};
