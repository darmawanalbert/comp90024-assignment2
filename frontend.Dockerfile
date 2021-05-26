# COMP90024 Team 1
# Albert, Darmawan (1168452) - Jakarta, ID - darmawana@student.unimelb.edu.au
# Clarisca, Lawrencia (1152594) - Melbourne, AU - clawrencia@student.unimelb.edu.au
# I Gede Wibawa, Cakramurti (1047538) - Melbourne, AU - icakramurti@student.unimelb.edu.au
# Nuvi, Anggaresti (830683) - Melbourne, AU - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah, Putra (1191132) - Jakarta, ID - wildananugra@student.unimelb.edu.au

# Install dependencies only when needed
FROM node:14.16.1-alpine AS deps
# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine to understand why libc6-compat might be needed.
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn install --frozen-lockfile

# Rebuild the source code only when needed
FROM node:14.16.1-alpine AS builder
WORKDIR /app
COPY frontend/ /app/
COPY --from=deps /app/node_modules ./node_modules
RUN yarn build

# Production image, copy all the files and run next
FROM node:14.16.1-alpine AS runner
WORKDIR /app

ENV NODE_ENV production

# You only need to copy next.config.js if you are NOT using the default configuration
# COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
RUN chown -R nextjs:nodejs /app/.next
USER nextjs

EXPOSE 3000

# Next.js collects completely anonymous telemetry data about general usage.
# Learn more here: https://nextjs.org/telemetry
# Uncomment the following line in case you want to disable telemetry.
# RUN npx next telemetry disable

CMD ["yarn", "start"]
