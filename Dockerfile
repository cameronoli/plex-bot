FROM node:lts-alpine3.14
WORKDIR /home/node/app
COPY . .
EXPOSE 80
RUN npm install discord.js
CMD ["node", "bot.js"]