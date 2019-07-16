import boto3
import _thread
import json, time
import sys, traceback
import configparser
#from replicate import Replicate

configParser = configparser.RawConfigParser()   
configFilePath = r'config.ini'
configParser.read(configFilePath)

region = configParser.get('sqs', 'region_name')
access_key = configParser.get('sqs', 'aws_access_key_id')
secret_key = configParser.get('sqs', 'aws_secret_access_key')
queue = configParser.get('sqs', 'queue_url')
debug = False

sqs = boto3.client('sqs', region_name=region, aws_access_key_id=access_key,
                   aws_secret_access_key=secret_key)
queue_url = queue

def probe():
    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
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
    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    body = message['Body']
    msgAttr = message['MessageAttributes']
    stimuli = msgAttr['StimuliType']['StringValue']

    if(debug == True):
        print('\n*********************Debug Logs**************************\n')
        print('response: %s' % response)
        print('receipt_handle: %s' % receipt_handle)
        print('body: %s' % body)
        print('msgAttr: %s' % msgAttr)
        print('stimuli: %s' % stimuli)
        print('\n**********************************************************')
    
    if(stimuli == "word_list"):
        process_message(body)
        #print("Stimuli Type Word List")
        #print('body: %s' % body)
        # Delete received message from queue
        # sqs.delete_message(
        #     QueueUrl=queue_url,
        #     ReceiptHandle=receipt_handle
        # )

# Define a function for the thread
def poll(threadName, delay):
    count = 0
    while True:
        time.sleep(delay)
        try:
            probe()
            print("Probe SQS:: %s: %s" % (threadName, time.ctime(time.time())))
        except:
             print("Found a malformed message in Queue")
             print('-'*60)
             traceback.print_exc(file=sys.stdout)
             print('-'*60)

def process_message(body):
    # r = Replicate()
    # r.run(body)
    s = json.loads(body)
    print('-'*60)
    #print(s["contrasts"]["contrast1"]["contrast_id"])
    print(s['model_type'])
    print("")
    print('-'*60)

        #responsedata['contrastID'] = 
            # 
            #     contrastID: info.ContrastID,
            #     MNIStr: result['group']
            #     substr: subjstr
            #     pmaps: result['pmaps']

if __name__ == '__main__':
    try:
        for x in range(3):
            _thread.start_new_thread(poll, ("Thread-"+str(x), 1, ))
    except:
        print("Error: unable to start thread")

    while 1:
        pass