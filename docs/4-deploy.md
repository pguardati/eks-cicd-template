# CodeBuild: how to build and deploy a Docker Image

## Send Jwt Secret to parameter store:
```
aws ssm put-parameter --name JWT_SECRET --value "YourJWTSecret" --type SecureString
```

## Check codebuild run:
CodeBuild is triggered every commit:
check the aws console.

## Check that the application can decode the token:
Get the public ip of the service
```
kubectl get services --all-namespaces
```
Check if the token is retrievable
```
PUBLIC_IP=a08d7322c3a4b45b9bb95a47987094c7-342059003.us-west-2.elb.amazonaws.com
curl -d '{"email":"'wolf@thedoor.com'","password":"huff-puff"}' -H "Content-Type: application/json" -X POST $PUBLIC_IP/auth
```
Get the token and the private content
```
TOKEN=`curl -d '{"email":"'wolf@thedoor.com'","password":"huff-puff"}' -H "Content-Type: application/json" -X POST $PUBLIC_IP/auth  | jq -r '.token'`
curl --request GET ''$PUBLIC_IP'/contents' -H "Authorization: Bearer ${TOKEN}" | jq 
```
