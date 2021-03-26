module.exports = {
	purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
	darkMode: false, // or 'media' or 'class'
	theme: {
		extend: {
			animation: {
				'skeleton-shimmer': 'skeleton-shimmer 1s linear infinite',
			},
			keyframes: {
				'skeleton-shimmer': {
					'0%': { transform: 'translateX(-100%)' },
					'100%': { transform: 'translateX(200%)' },
				},
			},
		},
	},
	variants: {
		extend: {},
	},
	plugins: [],
};
