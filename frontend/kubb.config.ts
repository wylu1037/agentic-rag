import { defineConfig } from "@kubb/core";
import { pluginOas } from "@kubb/plugin-oas";
import { pluginTs } from "@kubb/plugin-ts";
import { pluginClient } from "@kubb/plugin-client";

export default defineConfig({
  root: ".",
  input: { path: "./openapi.json" },
  output: { path: "./gen" },
  plugins: [
    pluginOas(),
    pluginTs({ output: { path: "models" } }),
    pluginClient({
      output: { path: "clients" },
    }),
  ],
});
