# Exercise 3: Scaling Flask app with ReplicaSets

Built a flash-sale Flask app image, loaded it into Minikube and ran it with a ReplicaSet (3 replicas), then scaled to 5 and tested self-healing.

## Files
- app.py, Dockerfile, flashsale-replicaset.yaml
- *-output.txt / pods-*.txt / rs-*.txt: kubectl outputs at each stage

## Q&A
1. Initial replicas: 3
2. Pods running after applying the ReplicaSet: 3
3. Scaling to 5: Kubernetes created 2 additional pods, so 5 are running.
4. Deleting a pod: the ReplicaSet automatically created a replacement to keep 5.
5. How the count is maintained: Kubernetes continuously compares running pods with the desired count and creates or deletes pods to match.
6. Nodes running: 1
7. Pod placement: all 5 pods run on the single node (minikube).
