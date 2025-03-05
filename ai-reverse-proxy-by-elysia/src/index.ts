import { Elysia } from 'elysia';
import { proxyHandler } from './handlers/proxyHandler';
import { healthCheck } from './health';

const app = new Elysia()
  .use(healthCheck)
  .use(proxyHandler)
  .listen(process.env.PORT || 3000);

console.log(`🚀 Reverse proxy server is running at ${app.server?.hostname}:${app.server?.port}`);
