# Exercise 1: Hello Pod

Deployed an Nginx pod on Minikube and exposed it as a NodePort service.

## Commands run
```
minikube start --driver=docker
kubectl run hello-k8s --image=nginx --port=80
kubectl get pods
kubectl expose pod hello-k8s --type=NodePort --port=80
minikube service hello-k8s
```

## Result
The Nginx welcome page opened in the browser (see nginx-welcome.png). Pod and service output are in pods-output.txt and service-output.txt.
