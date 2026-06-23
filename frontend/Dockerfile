# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package manifest files
COPY package*.json ./

# Install dependencies (if any)
RUN npm install

# Copy source code and config files
COPY . .

# Run the build script to compile to 'dist/'
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built static assets from build stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
