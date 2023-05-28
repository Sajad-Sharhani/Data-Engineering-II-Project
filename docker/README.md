
# Kubernetes cluster

The master node is vm3. From this vm you can run all the commands specified in this readme.

## Editing the script and saving the changes

The scripts that are run in the cluster are "consumer/consumer.py" and "producer/producer.py".

If you have made changes to these scripts you have to distribute these changes to all nodes.

You do this with the command "docker compose build && docker compose push". Make sure you are in the docker/ folder.

I think you need to restart the cluster after pushing the changes.

## Starting the cluster

Start the cluster by using the command "./start.sh".

## Stopping the cluster

Stop the cluster by using the command "./stop.sh"

## Accessing the MongoDB

When the cluster is running, the mongodb instance can be accesed on ip 192.168.2.93 (or localhost if you're on vm3) and port 30007.

There is a sample analysis script "analysis.py" which connects to the db so you can see how to do it.
