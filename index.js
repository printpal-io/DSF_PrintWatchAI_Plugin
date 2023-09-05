'use strict'

import { registerRoute } from '@/routes'

import PrintWatch from './PrintWatch.vue'

// Register a route via Plugins -> Print Watch
registerRoute(PrintWatch, {
	Plugins: {
		PrintWatch: {
			icon: 'mdi-eye',
			caption: 'PrintWatch AI',
			translated: true,
			path: '/PrintWatch'
		}
	}
});
