import boto3
import _thread
import json
import time
import sys
import traceback
from hubs.config import Config
from models.experiment import Experiment
from constant import *
from hubs.logger import Logger

region = Config.region_name
access_key  = Config.aws_access_key_id
secret_key = Config.aws_secret_access_key
sqs_url = Config.sqs_url
sqs = boto3.client('sqs', region_name=region, aws_access_key_id=access_key,
                   aws_secret_access_key=secret_key)
# sqs = boto3.client('sqs')

# print("sqs client = ",sqs)


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
        WaitTimeSeconds=5
    )
    if not response or response.get('Messages', None) is None:
        return
    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    body = message['Body']
    msgAttr = message['MessageAttributes']
    stimuli = msgAttr['StimuliType']['StringValue']

    if(Config.debug == True):
        log_info = ' ******** response: {0} ********'.format(response)
        Logger.debug(log_info)
        log_info = ' ******** receipt_handle:{0} ********'.format(receipt_handle)
        Logger.debug(log_info)
        log_info = ' ******** body:{0} ********'.format(body)
        Logger.debug(log_info)
        log_info = ' ******** msgAttr:{0} ********'.format(msgAttr)
        Logger.debug(log_info)
        log_info = ' ******** stimuli:{0} ********'.format(stimuli)
        Logger.debug(log_info)

    if(stimuli == WORD_LIST):
        info = json.loads(body)
        Experiment()(info)
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )

# Define a function for the thread
def poll(delay):
    while True:
        time.sleep(delay)
        try:
            probe()
            log_info = ' ******** Probe SQS:: {0} ********'.format(
                time.ctime(time.time()))
            Logger.debug(log_info)
        except:
            log_info = ' ******** Error Happened when processing the message  ********'
            Logger.debug(log_info)


if __name__ == '__main__':
    poll(5)
