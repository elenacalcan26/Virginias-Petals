#!/bin/sh

kubectl label nodes virginia-cluster-control-plane ingress-ready=true

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

# cd k8s/ingress
# kubectl apply -f ingress-rules.yml

# kubectl port-forward service/ingress-nginx-controller -n ingress-nginx 8000:80
