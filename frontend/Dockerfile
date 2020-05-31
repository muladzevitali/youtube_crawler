FROM node:12.10.0

# set working directory
WORKDIR /usr/src/frontend

# install and cache app dependencies
COPY package.json .
RUN npm install --silent
RUN npm install react-scripts -g --silent

ENV PATH /usr/src/frontend/node_modules/.bin:$PATH
COPY . .