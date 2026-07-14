// @ts-check
import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import tailwind from "@astrojs/tailwind";

// https://astro.build/config
export default defineConfig({
  // Default GitHub Pages project hosting: coderturtle.github.io/closed-book/.
  // No custom domain/DNS for this workshop, same precedent as borrow-native.
  // Every internal link MUST be base-aware (import.meta.env.BASE_URL), not a
  // bare "/path" - the single most common Pages-project breakage.
  site: "https://coderturtle.github.io",
  base: "/closed-book/",
  integrations: [mdx(), tailwind()],
  output: "static",
});
