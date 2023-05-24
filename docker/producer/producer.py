import pulsar
import sys

print("started", file=sys.stderr, flush=True)
client = pulsar.Client('pulsar://pulsar:6650')

print("connected", file=sys.stderr, flush=True)

producer = client.create_producer('my-topic')

print("created producer", file=sys.stderr, flush=True)

while True:
        producer.send(('Hello').encode('utf-8'))
        print("sent msg", file=sys.stderr, flush=True)

client.close()
