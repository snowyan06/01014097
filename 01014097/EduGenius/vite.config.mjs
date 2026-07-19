import { fileURLToPath, URL } from 'node:url';

import { PrimeVueResolver } from '@primevue/auto-import-resolver';
import vue from '@vitejs/plugin-vue';
import Components from 'unplugin-vue-components/vite';
import { defineConfig } from 'vite';

// https://vitejs.dev/config/
export default defineConfig({
    optimizeDeps: {
        noDiscovery: true,
        include: ['jszip','echarts'],
    },
    plugins: [
        vue(),
        Components({
            resolvers: [PrimeVueResolver()]
        })
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        }
    },
    server: {
           port: 5173,
           proxy: {
               '/api': {
                   target: 'http://localhost:8080',
                   changeOrigin: true
               },
               '/ai-api': {
                   target: 'http://localhost:8000',
                   changeOrigin: true,
                   rewrite: (path) => path.replace(/^\/ai-api/, '')
               }
           }
       }
});
