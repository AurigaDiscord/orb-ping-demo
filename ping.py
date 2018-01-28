#!/usr/bin/env python3

import os
import logging
import pika
import json

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO)

logging.info("Starting ping-demo orb")

MQ_PATH = os.environ['AMQP_PATH']
MQ_EXCHANGE = "auriga.{0}".format(os.environ['AMQP_EXCHANGE'])
MQ_KEY = "auriga.{0}".format(os.environ['AMQP_KEY_MESSAGE'])
MQ_KEY_OUTCOMING = "auriga.{0}".format(os.environ['AMQP_KEY_OUTCOMING'])
MQ_TOPIC_INCOMING = "{0}.{1}".format(MQ_EXCHANGE, os.environ['AMQP_QUEUE_INCOMING'])


def consume_callback(chan, method, properties, payload):
    decoded = json.loads(payload)
    if decoded['content'] != "ping":
        return
    channel_id = decoded['channel_id']
    response = {"type": "text", "channel_id": channel_id, "content": "pong"}
    encoded_response = json.dumps(response)
    chan.basic_publish(exchange=MQ_EXCHANGE,
                       routing_key=MQ_KEY_OUTCOMING,
                       body=encoded_response)
    return


params = pika.URLParameters(MQ_PATH)
connection = pika.BlockingConnection(params)
chan = connection.channel()

chan.queue_declare(queue=MQ_TOPIC_INCOMING, auto_delete=True)
chan.queue_bind(exchange=MQ_EXCHANGE, queue=MQ_TOPIC_INCOMING, routing_key=MQ_KEY)

chan.basic_consume(consume_callback, queue=MQ_TOPIC_INCOMING, no_ack=True)

chan.start_consuming()
