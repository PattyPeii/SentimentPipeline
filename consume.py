import pika
import json
import sys
from core import save_db
from config import config
from core import run_sentiment

connection = pika.BlockingConnection(
    pika.URLParameters(config["host"]))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [comment]\n" % sys.argv[0])
    sys.exit(1)
for severity in severities:
    channel.queue_bind(
        exchange='direct_logs', queue=queue_name, routing_key=severity)

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

