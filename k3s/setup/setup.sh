#!/bin/bash
# Script to run the Hetzner K3s Ansible playbook

# Ensure required packages are installed
if ! command -v ansible &> /dev/null; then
    echo "Ansible not found. Installing..."
    pip install ansible
fi

if ! pip list | grep hcloud > /dev/null; then
    echo "Installing Hetzner Cloud Python library..."
    pip install hcloud
fi

# Check if Helm is installed
if ! command -v helm &> /dev/null; then
    echo "Helm not found. Installing..."
    curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
    chmod 700 get_helm.sh
    ./get_helm.sh
    rm get_helm.sh
fi

# Check if Hetzner API token is set
if [ -z "$HETZNER_API_TOKEN" ]; then
    echo "Error: HETZNER_API_TOKEN environment variable is not set."
    echo "Please set it using: export HETZNER_API_TOKEN='your-api-token'"
    exit 1
fi

echo "Running Ansible playbook to provision Hetzner server and install K3s..."
ansible-playbook -i ./inventory.ini hetzner_k3s.yaml -e "hetzner_api_token=$HETZNER_API_TOKEN"


KUBECONFIG=$(pwd)/../k3s-kubeconfig.yaml kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.3/cert-manager.yaml
KUBECONFIG=$(pwd)/../k3s-kubeconfig.yaml kubectl apply ./issuer.yaml

# Check if kubeconfig file was created
if [ -f ./k3s-kubeconfig.yaml ]; then
    echo "====================================================================="
    echo "Setup completed successfully!"
    echo "To use kubectl with your new cluster, run:"
    echo "export KUBECONFIG=$(pwd)/../k3s-kubeconfig.yaml"
    echo "====================================================================="
else
    echo "Warning: kubeconfig file not found. There may have been an issue with the installation."
fi
