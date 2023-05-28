#!/bin/bash

# Apply Kubernetes manifests
sudo k3s kubectl apply -f pulsar-deployment.yaml
sudo k3s kubectl apply -f mongodb-deployment.yaml
sudo k3s kubectl apply -f producer-deployment.yaml
sudo k3s kubectl apply -f pulsar-service.yaml
sudo k3s kubectl apply -f consumer-deployment.yaml
sudo k3s kubectl apply -f mongodb-service.yaml

sudo k3s kubectl scale deploy pulsar --replicas=1
sudo k3s kubectl scale deploy mongodb --replicas=1
sudo k3s kubectl scale deploy producer --replicas=1
#sudo k3s kubectl scale deploy pulsar-service.yaml --replicas=1
sudo k3s kubectl scale deploy consumer --replicas=4
#sudo k3s kubectl scale deploy pulsar-service.yaml --replicas=1

#sudo kubectl port-forward service/mongodb 27017:27017 &

echo "Kubernetes cluster started successfully!"
