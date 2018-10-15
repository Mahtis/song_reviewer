FROM node:8.12.0

RUN mkdir -p /usr/src/app/frontend
COPY . /usr/src/app/frontend
WORKDIR /usr/src/app/frontend

RUN npm i

RUN npm run build
RUN npm install -g serve

WORKDIR /usr/src/app
RUN rm -r /usr/src/app/frontend

EXPOSE 5000

CMD ["serve", "-s", "-l", "5000", "build"]