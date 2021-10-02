FROM node:lts-alpine3.14
WORKDIR /home/node/app
COPY . /home/node/app
EXPOSE 80
RUN npm install -r npmRequirements.txt
CMD ["node", "bot.js"]