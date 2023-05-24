import sys
print("init", file=sys.stderr, flush=True)

import pulsar


print("started", file=sys.stderr, flush=True)
client = pulsar.Client('pulsar://pulsar:6650')

print("connected", file=sys.stderr, flush=True)

consumer = client.subscribe('my-topic', 'my-subscription')

print("created consumer", file=sys.stderr, flush=True)

while True:
        msg = consumer.receive()
        try:
            print("Received message '{}' id='{}'".format(msg.data(), msg.message_id()), file=sys.stderr, flush=True)
            # Acknowledge successful processing of the message
            consumer.acknowledge(msg)
        except Exception:
            # Message failed to be processed
            consumer.negative_acknowledge(msg)

client.close()
