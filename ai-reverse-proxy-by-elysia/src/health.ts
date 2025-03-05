import { Elysia } from "elysia"; 

export const healthCheck = new Elysia().get("/health", () => ({ status: "ok" }));
