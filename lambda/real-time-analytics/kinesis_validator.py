import base64
import json


def lambda_handler(event, context):
    output = []

    for record in event['records']:
        payload = base64.b64decode(record['data'])


        value = json.loads(payload)['value']
        if (value=="red"):
            result = "Dropped"
        else:
            result = "Ok"

        print ("Value: " + value + ", status: " + result);


        output_record = {
            'recordId': record['recordId'],
            'result': result,
            'data': base64.b64encode(payload)
        }
        output.append(output_record)

    print('Successfully processed {} records.'.format(len(event['records'])))

    return {'records': output}
