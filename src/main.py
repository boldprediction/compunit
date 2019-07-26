import os
import time
import json
import boto3
from constant import *
from hubs.logger import Logger
from hubs.config import Config
from hubs.subjects import Subjects
from models.experiment import Experiment
from constant import LOG_DIR, PID_FILE

inputs = {u'contrasts': {u'contrast1': {u'condition1': [u'cond1'], u'figures': [], u'condition2': [u'cond2'], u'coordinates': []}}, u'stimuli': {u'cond1': {u'type': u'word_list', u'value': u'one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, twenty, thirty, forty, fifty, hundred, thousand, million, half, quarter, pair, few, several, many, some, less, more'}, u'cond2': {u'type': u'word_list', u'value': u'house, building, hotel, office, parking, lot, park, street, road, sidewalk, highway, path, field, mountain, forest, beach, cinema, restaurant, bistro, shop, store'}}, u'DOI': u'', u'coordinate_space': u'mni', u'do_perm': False}


class Main:

    def __init__(self):

        with open(os.path.join(LOG_DIR, PID_FILE), 'w') as f:
            f.write(str(os.getpid())+'\n')

        Logger.info("Loading subjects in advance ... [@performance]")
        begin_time = time.time()
        __ = Subjects.english1000
        Logger.info("Loading subjects finished, time cost: "+str(time.time() - begin_time)+" s [@performance]")

        self.sqs_url = Config.sqs_url
        self.region = Config.region_name
        self.access_key = Config.aws_access_key_id
        self.secret_key = Config.aws_secret_access_key
        self.sqs = boto3.client('sqs', region_name=self.region, aws_access_key_id=self.access_key,
                   aws_secret_access_key=self.secret_key)

    def probe(self):
        # Receive message from SQS queue
        response = self.sqs.receive_message(
            QueueUrl=self.sqs_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=1,
            MessageAttributeNames=['StimuliType'],
            VisibilityTimeout=0,
            WaitTimeSeconds=10
        )
        if not response or response.get('Messages', None) is None:
            return None
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        message_id = message['MessageId']
        body = message['Body']
        msg_attrs = message['MessageAttributes']
        stimuli = msg_attrs['StimuliType']['StringValue']

        if stimuli == WORD_LIST:
            info = json.loads(body)
            self.sqs.delete_message(
                QueueUrl=self.sqs_url,
                ReceiptHandle=receipt_handle
            )
            Experiment()(info)
        return message_id

    def start(self):
        while True:
            try:
                message_id = self.probe()
                if message_id is not None:
                    Logger.info("Successfully process message" + message_id)
                else:
                    Logger.info("Didn't receive any message")
            except Exception as e:
                Logger.error(e)
                return


if __name__ == "__main__":
    Main().start()
