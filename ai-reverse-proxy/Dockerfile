FROM oven/bun:latest

WORKDIR /app

# Copy package files for install
COPY package.json .
COPY bun.lockb* .

# Install dependencies
RUN bun install --frozen-lockfile

# Copy source files
COPY src/ src/
COPY tsconfig.json .

# Set environment to production
ENV NODE_ENV production
ENV PORT 3000

# Expose the port the app runs on
EXPOSE 3000

# Create a health check endpoint
RUN echo 'import { Elysia } from "elysia"; export const healthCheck = new Elysia().get("/health", () => ({ status: "ok" }));' > src/health.ts

# Update index.ts to include health check
RUN echo 'import { Elysia } from "elysia";\nimport { proxyHandler } from "./handlers/proxyHandler";\nimport { healthCheck } from "./health";\n\nconst app = new Elysia()\n  .use(healthCheck)\n  .use(proxyHandler)\n  .listen(process.env.PORT || 8181);\n\nconsole.log(`🚀 Reverse proxy server is running at ${app.server?.hostname}:${app.server?.port}`);' > src/index.ts

# Command to run the application
CMD ["bun", "src/index.ts"]
