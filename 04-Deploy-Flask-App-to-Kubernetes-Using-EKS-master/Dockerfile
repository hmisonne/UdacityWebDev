FROM python:stretch

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "-b", ":8080", "main:APP"]


# export TOKEN=`curl -d '{"email":"<EMAIL>","password":"<PASSWORD>"}' -H "Content-Type: application/json" -X POST localhost:80/auth  | jq -r '.token'`
# curl --request GET 'http://127.0.0.1:80/contents' -H "Authorization: Bearer ${TOKEN}" | jq .

# curl --request GET 'http://127.0.0.1:80/contents' -H "Authorization: Bearer `curl -d '{"email":"test@gmail.com","password":"test"}' -H "Content-Type: application/json" -X POST localhost:80/auth  | jq -r '.token'`" | jq .

# docker run -p 80:8080 jwt-api-test --e=env_file