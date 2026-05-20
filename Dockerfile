# Stage 1: Install dependencies
FROM node:20-alpine AS deps

WORKDIR /app

# Install necessary OS packages
RUN apk add --no-cache libc6-compat openssl

# Copy package files
COPY package.json package-lock.json* ./

# Install node_modules
RUN npm install

# Stage 2: Build application
FROM node:20-alpine AS builder

WORKDIR /app

# Copy files and install dependencies
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Generate Prisma client
RUN npx prisma generate

# Optional: Build Next.js app (if you're planning a production image)
# RUN npm run build

# Stage 3: Runtime
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=development

# Copy only required files
COPY --from=builder /app ./

# Expose Next.js default port
EXPOSE 3000

# Default dev command (can be overridden in docker-compose)
CMD ["npm", "run", "dev"]
