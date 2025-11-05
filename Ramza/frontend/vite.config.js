import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/media': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    },
    // Add history API fallback for SPA
    fs: {
      strict: false
    }
  },
  // Add base configuration for SPA
  base: '/',
  // Add build configuration for SPA
  build: {
    rollupOptions: {
      output: {
        manualChunks: undefined
      }
    }
  }
})