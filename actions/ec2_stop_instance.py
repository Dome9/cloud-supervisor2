import boto3

### Turn off EC2 instance ###
def run_action(boto_session,rule,entity,params):
    instance = entity['id']
    ec2 = boto_session.client('ec2')
    result = ec2.stop_instances(InstanceIds=[instance])

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = "Instance stopped: %s \n" % instance

    return text_output 


