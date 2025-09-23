import { defineConfig,loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd())
  return {
    plugins: [react()],
    server: {
      host: '0.0.0.0',
      port: 5173,
      allowedHosts: true
    },
    define: {
      __API_BASE__: JSON.stringify(env.VITE_API_BASE)
    }
  }
})