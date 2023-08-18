import { defineConfig } from "vite";

export default defineConfig ({
 build: {
    outDir: "./src/static/javascript/vite",
    rollupOptions: {
      output: {
        entryFileNames: '[name].js',
        chunkFileNames: '[name].js',
      }
    }
  } 
})