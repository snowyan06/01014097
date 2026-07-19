module.exports = {
    content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                primary: {
                    light: '#10B981',
                    medium: '#2E8B6F',
                    DEFAULT: '#0A5C4B',
                    dark: '#064E3B'
                },
                surface: {
                    0: '#FFFFFF',
                    50: '#F9FAFB',
                    100: '#F3F4F6'
                }
            },
            fontFamily: {
                sans: ['HarmonyOS Sans', 'PingFang SC', 'Microsoft YaHei', 'sans-serif']
            }
        }
    },
    plugins: []
};
