import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Ensure assets use relative paths so they load correctly from inside the PyInstaller bundle.
export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    assetsDir: 'assets'
  }
});
