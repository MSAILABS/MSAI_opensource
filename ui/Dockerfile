FROM node:20-alpine AS ui

WORKDIR /ui

# Copy package.json and package-lock.json separately for better caching
COPY package*.json ./

RUN npm install

COPY . .

# Build the application
RUN npm run build

# Set the default command to start the application
CMD ["npm", "start"]
