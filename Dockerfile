FROM node:lts-alpine3.14
WORKDIR /home/node/app
EXPOSE 80
CMD ["node", "bot.js"]