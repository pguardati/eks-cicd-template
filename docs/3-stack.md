# CloudFormation: how to create a stack of resources to trigger a cicd pipeline

# 1 - Generate github access token
Settings -> developer settings -> access token -> access to private repo

# 2 - Add default values to the parameters in the code pipeline 
Modify `cloud-formation.yml`:
```
EksClusterName : use the name of the EKS cluster you created above
GitSourceRepo : use the name of your project's github repo.
GitHubUser : use your github user name
KubectlRoleName : use the name of the role you created for kubectl above
```

# 3 - Create the stack 
From the terminal, run:
```
aws cloudformation create-stack \
--stack-name simple-jwt-api-cicd \
--template-body file://$REPOSITORY_PATH/cicd/cloud-formation.yml \
--parameters ParameterKey=GitHubToken,ParameterValue=$GithubToken \
ParameterKey=GitBranch,ParameterValue=master \
--capabilities CAPABILITY_IAM
```

-- 
Note:  
If cloud formation get stacked, delete the stack.  
Then go to lambda function and copy the resource name,  
Eventually, run:
```
aws lambda delete-function --function-name $LambdaFunctionResourceId
```

