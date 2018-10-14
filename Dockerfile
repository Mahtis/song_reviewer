FROM node:8.12.0

RUN apt-get update && \
    apt-get install -y python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
COPY . /usr/src/app
WORKDIR /usr/src/app/frontend

RUN npm install

RUN npm run build

WORKDIR /usr/src/app/backend

RUN rm -r /usr/src/app/frontend
RUN rm -r /usr/src/app/backend/static
RUN mv /usr/src/app/backend/build/static /usr/src/app/backend/

# execute everyone's favorite pip command, pip install -r
RUN pip3 install -r requirements.txt

EXPOSE 8000

# execute the Flask app
CMD ["python3", "app.py"]