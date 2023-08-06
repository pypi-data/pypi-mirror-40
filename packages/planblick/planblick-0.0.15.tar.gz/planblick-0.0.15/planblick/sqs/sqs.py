import json
import os
import boto3
import threading
from time import sleep


class Sqs:

    def __init__(self, QueueName=None, Attributes={"VisibilityTimeout": "60"}):
        self.ENVIRONMENT = json.loads(os.getenv("CLUSTER_CONFIG")).get("environment")
        boto3.setup_default_session(region_name='eu-central-1')
        self.sqs = boto3.resource('sqs')

        if QueueName is not None:
            self.set_queue(QueueName=QueueName, Attributes=Attributes)

    def get_all_queues(self):
        for queue in self.sqs.queues.all():
            print(queue.url)

    def set_queue(self, QueueName, Attributes=None):
        try:
            self.queue = self.sqs.get_queue_by_name(QueueName=QueueName)
        except Exception as e:
            print(e.response.get("Error").get("Code"))
            if e.response.get("Error").get("Code") == "AWS.SimpleQueueService.NonExistentQueue":
                print("Trying to auto-create queue...")
                self.create_queue(QueueName=QueueName, Attributes=Attributes)
            else:
                raise
        return True

    def create_queue(self, QueueName, Attributes={}):
        try:
            self.queue = self.sqs.create_queue(QueueName=QueueName, Attributes=Attributes)
        except Exception as e:
            print(e.response.get("Error").get("Code"))
            if e.response.get("Error").get("Code") == "AWS.SimpleQueueService.QueueDeletedRecently":
                print("Waiting 60 seconds and try again automatically...")
                sleep(62)
                self.queue = self.sqs.create_queue(QueueName=QueueName, Attributes=Attributes)
            else:
                raise

        print("Queue '{0}' created successfully!".format(QueueName))

    def send(self, MessageBody, MessageAttributes={}):
        if type(MessageBody) == dict:
            MessageBody = json.dumps(MessageBody)
        self.queue.send_message(MessageBody=MessageBody, MessageAttributes=MessageAttributes)

        return True

    def receive(self, callback=None, MessageAttributeNames=[], endless=False):
        while (1):
            for message in self.queue.receive_messages(MessageAttributeNames=MessageAttributeNames):
                if callback is not None:
                    result = callback(message)
                else:
                    result = self.handleMessage(message)
                if result == True:
                    message.delete()
            if endless is not True:
                break

    def handleMessage(self, message):
        print(
            "No Message-Handler-Provided. Please use this class, extend from it and implement your own handleMessage funktion")
        return False

    def addConsumer(self, callback, MessageAttributeNames=[]):
        t = threading.Thread(target=self.receive, args=([callback, MessageAttributeNames, True]))
        t.daemon = True
        t.start()


# Create your own class which extends from this and implement your handleMessage function which will be called for new functions
# Example:
class Example(Sqs):
    def __init__(self, QueueName, Attributes={}):
        super().__init__(QueueName, Attributes)

    def log(self, message):
        print(self)
        print("Received Message!!!")
        print(message.body)

    def handleMessage(self, message):
        self.log(message)
        return True
