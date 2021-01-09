# 2. EKS: how to create a Kubernetes cluster

## Setup the local machine with utils for aws and kubernetes
0 - install aws cli  
1 - create eks-user  
2 - store credentials into ~/.aws  
3 - install utils for eks:  
```
brew tap weaveworks/tap
brew install weaveworks/tap/eksctl
```

## Create eks cluster - note: ETA ~10' 
```
eksctl create cluster --name eks-cluster
```

## Create a role to assign to eks cluster
1 - Get the current aws id 
```
aws sts get-caller-identity --query Account --output text
```

2 - Create a policy document `config/trust.json` to allow 
root user to change role to EKS Cluster
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::112233:root"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```
3 - Create a role with that policy in aws
```
aws iam create-role --role-name FlaskDeployCBKubectlRole \
--assume-role-policy-document file://$REPOSITORY_PATH/config/trust.json \
--output text --query 'Role.Arn'
```
4 - Create a role policy `i-am-role-policy.json` to allow the `FlaskDeployCBKubectlRole` to interact with eks and ssm
```
{
 "Version": "2012-10-17",
 "Statement":[{
     "Effect": "Allow",
     "Action": ["eks:Describe*", "ssm:GetParameters"],
     "Resource":"*"
 }]
}
```
5 - Update the policy
```
aws iam put-role-policy --role-name FlaskDeployCBKubectlRole --policy-name eks-describe \
--policy-document file://$REPOSITORY_PATH/config/i-am-role-policy.json
```

## Grant role access to the cluster
1 - Create configuration `config/aws-auth-patch.yml` to assign role to cluster
```
kubectl get -n kube-system configmap/aws-auth -o yaml > config/aws-auth-patch.yml
```
2 - Add the following group to the section `mapRoles` of `config/aws-auth-patch.yml`:
```
- groups:
  - system:masters
  rolearn: arn:aws:iam::112233:role/FlaskDeployCBKubectlRole
  username: build
```
3 - Update the role policy
```
kubectl patch configmap/aws-auth -n kube-system \
--patch "$(cat config/aws-auth-patch.yml)"
```

