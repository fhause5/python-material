import boto3, os

def lambda_handler(event, context):
    bucketsS3 = boto3.client('s3')
    try:
        results = bucketsS3.list_buckets()
        print(results)
        output = ""
        for i in results['Buckets']:
            output = output + i['Name'] + "<br>"
        return ("<h1><font color=green>s3 Bucket List:</h1><br><br>" + output)
    except:
        return("<h1><font> color=red>Error!</font></h1><br><br>" )