FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install && npm run build
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
