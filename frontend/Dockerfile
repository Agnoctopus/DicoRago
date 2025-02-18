# Builder
FROM node:23-alpine as builder
MAINTAINER Agno

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy application source code and build
COPY . .
RUN npm run build

# Final image
FROM nginx:1.27-alpine
MAINTAINER Agno

# Copy worker build web app directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80 for HTTP
EXPOSE 80

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
