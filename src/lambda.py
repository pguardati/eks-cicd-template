import json
import boto3
from botocore.vendored import requests


def handler(event, context):
    """When the stack is created, grant codebuild the access to an eks cluster

    Args:
        event(dict): descriptor of the event that triggered this handler
        context(Context): aws context object

    Returns:
        dict
    Example::
        class Context: pass
        event = {
            "RequestType": "Create",
            "ResponseURL": "http://pre-signed-S3-url-for-response",
            "StackId": "arn:aws:cloudformation:us-west-2:123456789012:stack/MyStack/guid",
            "RequestId": "unique id for this create request",
            "ResourceType": "Custom::TestResource",
            "LogicalResourceId": "MyTestResource",
            "ResourceProperties": {
                "StackName": "MyStack",
                "KubectlRoleName": "FlaskDeployCBKubectlRole",
                "CodeBuildServiceRoleArn": "arn:aws:iam::$YourAwsId:role/CodeBuildRole"
            }
        }
        context = Context()
        context.log_stream_name = "2021/01/07/[$LATEST]b1e39ebb851645758971da93325"
        handler(event,context)
    """
    response = {
        'Status': 'SUCCESS',
        "Reason": "See the details in CloudWatch Log Stream: " + context.log_stream_name,
        'PhysicalResourceId': context.log_stream_name,
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'Data': {"Message": "Resource creation successful!"},
    }

    client = boto3.client('iam')
    try:
        if event['RequestType'] == 'Create':
            # get eks role policy
            kubectl_role_name = event['ResourceProperties']['KubectlRoleName']
            assume = client.get_role(RoleName=kubectl_role_name)
            assume_doc = assume['Role']['AssumeRolePolicyDocument']

            # create a role list for codebuild
            build_role_arn = event['ResourceProperties']['CodeBuildServiceRoleArn']
            roles = [{'Effect': 'Allow', 'Principal': {'AWS': build_role_arn}, 'Action': 'sts:AssumeRole'}]

            # add the eks role to the codebuild role
            for statement in assume_doc['Statement']:
                if 'AWS' in statement['Principal']:
                    if statement['Principal']['AWS'].startswith('arn:aws:iam:'):
                        roles.append(statement)
            assume_doc['Statement'] = roles

            # update the policy of eks role
            update_response = client.update_assume_role_policy(
                RoleName=kubectl_role_name,
                PolicyDocument=json.dumps(assume_doc)
            )
    except Exception as e:
        print(e)
        response['Status'] = 'FAILED'
        response["Reason"] = e
        response['Data'] = {"Message": "Resource creation failed"}

    response_body = json.dumps(response)
    headers = {'content-type': '', "content-length": str(len(response_body))}
    put_response = requests.put(event['ResponseURL'], headers=headers, data=response_body)
    return response
