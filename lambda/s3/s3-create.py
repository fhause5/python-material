import boto3, os, time
import random
import string

def randomString(stringLength=3):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
randomStr = randomString(stringLength=3)
AWS_DEFAULT_REGION = "eu-central-1"
os.environ['AWS_DEFAULT_REGION'] = AWS_DEFAULT_REGION

bucketNameNew = "test-" + str(randomStr)

def lambda_handler(event, context):
    bucketsS3 = boto3.resource('s3')
    try:
        results = bucketsS3.create_bucket(
            Bucket=bucketNameNew,
            CreateBucketConfiguration={'LocationConstraint': AWS_DEFAULT_REGION}
        )
        return ("<h1><font color=green>s3 Bucket List:</h1><br><br>" + str(results))
    except:
        return("<h1><font> color=red>Error!</font></h1><br><br>" )
