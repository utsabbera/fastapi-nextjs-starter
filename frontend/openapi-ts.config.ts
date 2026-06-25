import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  client: "@hey-api/client-fetch",
  input: "../backend/openapi.json",
  output: {
    path: "src/lib/generated",
    format: "prettier",
    lint: "disabled",
  },
  types: { enums: "typescript" },
  services: { asClass: false },
});
