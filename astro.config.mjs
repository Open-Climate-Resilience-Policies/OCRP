import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://open-climate-resilience-policies.github.io',
  base: '/OCRP',
  outDir: './dist',
  build: {
    format: 'directory'
  }
});
