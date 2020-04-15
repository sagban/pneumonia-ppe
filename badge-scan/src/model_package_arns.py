class ModelPackageArnProvider:

    @staticmethod
    def get_model_package_arn(current_region):
        mapping = {
          "ap-south-1": "arn:aws:sagemaker:ap-south-1:077584701553:model-package/bar-qr-code-reader-1571413449-a35a47dda86b16474ecd69ff9f20b46f",
          "ap-northeast-2": "arn:aws:sagemaker:ap-northeast-2:745090734665:model-package/bar-qr-code-reader-1571413449-a35a47dda86b16474ecd69ff9f20b46f",
          "ap-southeast-1" : "arn:aws:sagemaker:ap-southeast-1:192199979996:model-package/bar-qr-code-reader-1571413449-a35a47dda86b16474ecd69ff9f20b46f",
          "ap-southeast-2" : "arn:aws:sagemaker:ap-southeast-2:666831318237:model-package/bar-qr-code-reader-1571413449-a35a47dda86b16474ecd69ff9f20b46f",
          "ap-northeast-1" : "arn:aws:sagemaker:ap-northeast-1:977537786026:model-package/bar-qr-code-reader-1571413449-a35a47dda86b16474ecd69ff9f20b46f",
          "ca-central-1" : "arn:aws:sagemaker:ca-central-1:470592106596:model-package/bar-qr-code-reader-1571413449-a35a47dda86b16474ecd69ff9f20b46f",
          "eu-central-1" : "arn:aws:sagemaker:eu-central-1:446921602837:model-package/bar-qr-code-reader-1571413449-a35a47dda86b16474ecd69ff9f20b46f",
          "eu-west-1" : "arn:aws:sagemaker:eu-west-1:985815980388:model-package/bar-qr-code-reader-1571413449-a35a47dda86b16474ecd69ff9f20b46f",
          "eu-west-2" : "arn:aws:sagemaker:eu-west-2:856760150666:model-package/bar-qr-code-reader-1571413449-a35a47dda86b16474ecd69ff9f20b46f",
          "eu-west-3" : "arn:aws:sagemaker:eu-west-3:843114510376:model-package/bar-qr-code-reader-1571413449-a35a47dda86b16474ecd69ff9f20b46f",
          "eu-north-1" : "arn:aws:sagemaker:eu-north-1:136758871317:model-package/bar-qr-code-reader-1571413449-a35a47dda86b16474ecd69ff9f20b46f",
          "sa-east-1" : "arn:aws:sagemaker:sa-east-1:270155090741:model-package/bar-qr-code-reader-1571413449-a35a47dda86b16474ecd69ff9f20b46f",
          "us-east-1" : "arn:aws:sagemaker:us-east-1:865070037744:model-package/bar-qr-code-reader-1571413449-a35a47dda86b16474ecd69ff9f20b46f",
          "us-east-2" : "arn:aws:sagemaker:us-east-2:057799348421:model-package/bar-qr-code-reader-1571413449-a35a47dda86b16474ecd69ff9f20b46f",
          "us-west-1" : "arn:aws:sagemaker:us-west-1:382657785993:model-package/bar-qr-code-reader-1571413449-a35a47dda86b16474ecd69ff9f20b46f",
          "us-west-2" : "arn:aws:sagemaker:us-west-2:594846645681:model-package/bar-qr-code-reader-1571413449-a35a47dda86b16474ecd69ff9f20b46f" 
        }
        return mapping[current_region]