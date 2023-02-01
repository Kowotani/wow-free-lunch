# Build React static files
FROM node:16.17.0-alpine as build

WORKDIR /app/frontend
COPY ./wow_free_lunch/package.json ./
COPY ./wow_free_lunch/package-lock.json ./
RUN npm ci
COPY ./wow_free_lunch/ ./
RUN npm run build

# Copy React static files and start nginx
FROM nginx:stable-alpine
COPY --from=build /app/frontend/build /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]