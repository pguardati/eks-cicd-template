# Docker: how to containerise a flask API

- create a Docker image
```
docker build . -f cicd/Dockerfile -t jwt-api-test
```

- create the environment variables in `config/.env_file`:
```
JWT_SECRET='abc123abc1234'
LOG_LEVEL=INFO
```

- run the image locally
```
docker run \
--rm \
--env-file=config/.env_file \
-it \
-p 80:8080 \
jwt-api-test 
```

check if the api inside the docker is able to get a token:
```
TOKEN=`curl -d '{"email":"'wolf@thedoor.com'","password":"huff-puff"}' -H "Content-Type: application/json" -X POST 0.0.0.0:80/auth  | jq -r '.token'`
curl --request GET '0.0.0.0:80/contents' -H "Authorization: Bearer ${TOKEN}" | jq 
```
check if the api inside can authenticate a token:
```
PUBLIC_IP=0.0.0.0:80
curl -d '{"email":"'wolf@thedoor.com'","password":"huff-puff"}' -H "Content-Type: application/json" -X POST $PUBLIC_IP/auth
```

Note: 
To stop and remove every local container (brute force):
```
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
```

