import boto3
import _thread
import time
# from replicate import Replicate

debug = False
# Create SQS client
sqs = boto3.client('sqs', region_name='us-east-2', aws_access_key_id='AKIAUCO6FZLTYUHMK6OR',
                   aws_secret_access_key='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')

queue_url = 'https://sqs.us-east-2.amazonaws.com/280175692519/bold_sqs	'

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
    # message = response['Messages'][0]
    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    body = message['Body']
    msgAttr = message['MessageAttributes']
    stimuli = msgAttr['StimuliType']['StringValue']

    if(debug == True):
        print('\n***********************************************\n')
        print('response: %s' % response)
        print('\n***********************************************\n')
        print('receipt_handle: %s' % receipt_handle)
        print('\n***********************************************\n')
        print('body: %s' % body)
        print('\n***********************************************\n')
        print('msgAttr: %s' % msgAttr)
        print('\n***********************************************\n')
        print('stimuli: %s' % stimuli)
        print('\n**********************************************************************************************')
    if(stimuli == "word_list"):
        # r = Replicate()
        # r.run(body)
        print("Stimuli Type Word List")
        print('body: %s' % body)
        # Delete received message from queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )

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


if __name__ == '__main__':
    # poll()
    # Create two threads as follows

    try:
        for x in range(3):
            _thread.start_new_thread(poll, ("Thread-"+str(x), 1, ))
    except:
        print("Error: unable to start thread")

    while 1:
        pass
    # print_time()
