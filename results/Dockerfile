FROM node:current-slim

ENV NODE_ENV=production
WORKDIR /app
# Copy source code to /src in container
COPY package.json package.json
RUN npm install --production

COPY . .

# Document the port the app listens on
EXPOSE 8090

# Run this command (starts the app) when the container starts
CMD [ "node", "./app.js"]
