#!/bin/sh

kubectl apply -n portainer -f https://downloads.portainer.io/ce2-14/portainer.yaml

# kubectl port-forward service/portainer -n portainer 30777:9000
