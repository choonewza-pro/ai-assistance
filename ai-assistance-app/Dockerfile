# STATE 1: Builder
FROM node:20.17.0-alpine AS builder
WORKDIR /usr/src/app

RUN apk update && \
    apk add --no-cache tzdata

COPY ./package*.json ./
RUN npm install --frozen-lockfile
COPY --chown=node:node . .
RUN npm run build

# STATE 2: App
FROM node:20.17.0-alpine AS runner
WORKDIR /usr/src/app

RUN apk update && \
    apk add --no-cache tzdata

COPY --from=builder --chown=node:node /usr/src/app/next.config.ts ./
COPY --from=builder --chown=node:node /usr/src/app/public ./public
COPY --from=builder --chown=node:node /usr/src/app/.next ./.next
COPY --from=builder --chown=node:node /usr/src/app/package.json ./package.json
COPY --from=builder --chown=node:node /usr/src/app/package-lock.json ./package-lock.json
RUN npm install --production --frozen-lockfile
USER node

EXPOSE 3000
CMD ["npm", "start"]