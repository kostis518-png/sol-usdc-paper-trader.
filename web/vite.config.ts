import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "/sol-usdc-paper-trader./",
  plugins: [react()],
});
