#!/bin/bash

# Delete Kubernetes manifests
sudo k3s kubectl delete -f pulsar-deployment.yaml
sudo k3s kubectl delete -f mongodb-deployment.yaml
sudo k3s kubectl delete -f producer-deployment.yaml
sudo k3s kubectl delete -f pulsar-service.yaml
sudo k3s kubectl delete -f consumer-deployment.yaml
sudo k3s kubectl delete -f mongodb-service.yaml

echo "Kubernetes cluster stopped successfully!"
