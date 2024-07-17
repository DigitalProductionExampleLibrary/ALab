import { defineConfig } from "astro/config";
import remarkToc from "remark-toc";

// https://astro.build/config
export default defineConfig({
  redirects: {
    "/ALab": "ALab/main",
  },
  markdown: {
    remarkPlugins: [[remarkToc, { heading: "toc" }]],
  },
  site: "https://DigitalProductionExampleLibrary.github.io",
  base: "/ALab",
});
