from celery import Celery

app = Celery('simulate', backend='rpc://guest@localhost', broker = 'amqp://guest:@localhost')
app.config_from_object('django.conf:settings')