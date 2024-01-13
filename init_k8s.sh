#!/bin/sh

cd terraform
terraform init
terraform apply --auto-approve

cd ../k8s

cd pgadmin
kubectl apply -f configmap.yml
kubectl apply -f deployment.yml
kubectl apply -f services.yml

cd ../auth-db
kubectl apply -f configmap.yml
kubectl apply -f statefulset.yml
kubectl apply -f services.yml

cd ../auth-service
kubectl apply -f configmap.yml
kubectl apply -f deployment.yml
kubectl apply -f services.yml

cd ../flower-shop-db
kubectl apply -f configmap.yml
kubectl apply -f statefulset.yml
kubectl apply -f services.yml

cd ../core-service
kubectl apply -f configmap.yml
kubectl apply -f deployment.yml
kubectl apply -f services.yml

cd ../business-logic-service
kubectl apply -f deployment.yml
kubectl apply -f services.yml
