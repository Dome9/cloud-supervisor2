import boto3
import re

### Add Tags to EC2 ### 
# Tag format: AUTO: ec2_tag_instance key value
#Tags with spaces can be added if they are surrounded by quotes: ex: ec2_tag_instance "this is my key" "this is a value"
def run_action(rule,entity,params):
    instance = entity['id']
    region = entity['region']
    region = region.replace("_","-")

    if len(params) == 2: #Standard key value formatting
        key = params[0]
        value = params[1]

    else:
        #Bring the params together to parse and look for quotes
        both_tags = " ".join(params)

        if "\"" not in both_tags: 
            text_output = ("Tag \"%s\" does not follow formatting - skipping\n" % both_tags) # String is formatted wrong. Fail/exit
            return text_output

        #Capture text blocks in quotes or standalones
        pattern = re.compile("[(A-Za-z0-9_\.,\s-]*")

        matched_tags = re.findall(pattern, both_tags)
        both_tags_no_spaces = [x.strip(' ') for x in matched_tags] # Remove empty spaces in array
        both_tags_no_spaces[:] = [x for x in both_tags_no_spaces if x != ''] # Remove empty array elements
        
        key = both_tags_no_spaces[0]
        value = both_tags_no_spaces[1]

    ec2 = boto3.client('ec2', region_name=region)
    result = ec2.create_tags(
        Resources=[instance],
        Tags=[
            {
                'Key': key,
                'Value': value
            }
        ]
    )
    
    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = "Instance tagged: %s \nKey: %s | Value: %s \n" % (instance,key,value)

    return text_output




