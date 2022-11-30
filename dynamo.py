import boto3
import os
import base64

def retrieve_dynamo_secret(hash):
    kms = boto3.client("kms")
    dynamo = boto3.client("dynamodb")

    response = dynamo.get_item(
        TableName=os.environ["DYNAMO_NAME"],
        Key={
            "EntryHash": {
                "S": hash
            }
        }
    )

    decrypted = kms.decrypt(KeyId=os.environ["KEY_ARN"],
                            CiphertextBlob=base64.b64decode(response["Item"]["Value"]["S"].encode("utf-8")))
    return decrypted["Plaintext"].decode("utf-8")