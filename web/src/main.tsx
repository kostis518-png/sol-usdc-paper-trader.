import React from "react";
import ReactDOM from "react-dom/client";
import { PhantomProvider } from "@phantom/react-sdk";
import { AddressType } from "@phantom/browser-sdk";
import App from "./App";
import "./style.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <PhantomProvider
      config={{ providers: ["injected"], addressTypes: [AddressType.solana] }}
      appName="SOL/USDC Control Room"
    >
      <App />
    </PhantomProvider>
  </React.StrictMode>,
);