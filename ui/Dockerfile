FROM node:20-alpine AS ui

WORKDIR /ui

COPY . .

RUN npm install

RUN npm run build

CMD ["npm", "start"]
