import boto3
import json
from hubs.config import Config
from models.experiment import Experiment
from constant import *
from hubs.logger import Logger

region = Config.region_name
access_key = Config.aws_access_key_id
secret_key = Config.aws_secret_access_key
sqs_url = Config.sqs_url
sqs = boto3.client('sqs', region_name=region, aws_access_key_id=access_key,
                   aws_secret_access_key=secret_key)


def probe():
    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=sqs_url,
        AttributeNames=[
            'All'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'StimuliType'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=10
    )
    if not response or response.get('Messages', None) is None:
        return None
    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    message_id = message['MessageId']
    body = message['Body']
    msgAttr = message['MessageAttributes']
    stimuli = msgAttr['StimuliType']['StringValue']

    if(stimuli == WORD_LIST):
        info = json.loads(body)
        Experiment()(info)
        sqs.delete_message(
            QueueUrl=sqs_url,
            ReceiptHandle=receipt_handle
        )
    return message_id


# Define a function for the thread
def poll():
    while True:
        try:
            message_id = probe()
            if message_id is not None:
                log_info = "Successfully process message" + message_id
                Logger.debug(log_info)
            else:
                log_info = "Didn't receive any message"
                Logger.debug(log_info)
        except:
            log_info = "Error Happened when processing messages"
            Logger.debug(log_info)
            return 


if __name__ == '__main__':
    poll()
