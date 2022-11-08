import pika
import json
import sys
from core import save_db
from config import config
from core import run_sentiment

connection = pika.BlockingConnection(
    pika.URLParameters(config["host"]))
channel = connection.channel()

result = channel.queue_declare(queue="comment", exclusive=False)
queue_name = result.method.queue

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    json_body = json.loads(body)
    process_type = "create"
    if "_id" in json_body:
        process_type = "update"
    raw_msg = json_body["comment"]
    sentiment = run_sentiment.get_sentiment(config, raw_msg)
    sentiment_type = json.loads(sentiment)["type"]
    processed_msg = run_sentiment.construct_msg(json_msg=json_body, sentiment=sentiment_type)
    print(processed_msg)
    db = save_db.DB_CONNECT(config=config)
    if process_type == "update":
        db.update_msg(json_body["_id"], processed_msg)
    else:
        db.save_msg(processed_msg)

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

