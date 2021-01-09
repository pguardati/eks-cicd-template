# ShutDownOperation: how to delete the Cluster, the Stack of resources and the sensitive parameters

Delete CloudFormation stack:
```
aws cloudformation delete-stack --stack-name simple-jwt-api-cicd
```

Delete EKS Cluster:
```
eksctl delete cluster --name eks-cluster
```

Delete the secret from the aws paramter store:
```
aws ssm delete-parameter --name JWT_SECRET
```
