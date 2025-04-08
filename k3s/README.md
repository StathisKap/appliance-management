## K3s Cluster

K3s is a lightweight distribution of Kubernetes.

To use it you'll need `kubectl`. The `setup.sh` script installs it as well but you can also just `brew install kubectl`.

Then use the KUBECOFNIG in this file by setthing the variable to the path
```sb
KUBECONFIG="$(pwd)/k3s-kubeconfig.yaml"
```

Then run `kubectl get nodes` to check that it works.