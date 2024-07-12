import { defineConfig } from 'astro/config';
import remarkToc from 'remark-toc';

// https://astro.build/config
export default defineConfig({
  redirects: {
    '/': '/main',
  },
  markdown: {
    remarkPlugins: [[remarkToc, { heading: 'toc' }]],
  },
});
