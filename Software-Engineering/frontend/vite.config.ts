import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // http://frontend:5173/api/v1/* -> http://backend:8000/api/v1/*
      // '/api/v1/': 'http://127.0.0.1:8000',
    },
  },
})
