import os
import json
import boto3
import io
import base64
import numpy as np

# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime = boto3.client('runtime.sagemaker')


def lambda_handler(event, context):
    # TODO implement
    inv_mapping = {0: 'normal', 1: 'pneumonia', 2: 'COVID-19'}
    data = json.loads(json.dumps(event))
    img = data['data']
    print(data)
    s = base64.b64encode(img)
    imgdata = base64.b64decode(s)
    t = np.frombuffer(imgdata, np.float32)
    data = np.reshape(t, (1, 224, 224, 3))
    payload = json.dumps(data.tolist())
    response = client.invoke_endpoint(EndpointName=ENDPOINT_NAME, ContentType='application/json', Body=payload)
    prediction = json.loads(response['Body'].read().decode())
    pred_list = prediction['predictions'][0]
    max_index = pred_list.index(max(pred_list))
    result = inv_mapping[max_index]

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
