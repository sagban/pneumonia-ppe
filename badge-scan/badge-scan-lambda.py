import json
import boto3
import io
import os
import base64
# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime = boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    # TODO implement

    data = json.loads(json.dumps(event))
    base_img = data['data']
    payload = base64.b64decode(base_img)
    # Call your model for predicting which object appears in this image.
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType='application/x-image',
        Body=payload
    )
    # read the prediction result and parse the json
    result = response['Body'].read().decode()
    print(result)
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
