# Hetzner CX22 with K3s

This project contains Ansible playbooks to automate the deployment of a CX22 server on Hetzner Cloud and install K3s on it.

## Prerequisites

- Ansible installed on your local machine
- Hetzner Cloud account with API token
- SSH key uploaded to your Hetzner Cloud account

## Setup

1. Set your Hetzner API token as an environment variable:

```bash
export HETZNER_API_TOKEN='your-api-token'
```

2. Review and modify the `hetzner_k3s.yaml` playbook if needed:
   - Update the `server_name` if you want a different name
   - Change the `server_location` if you prefer another datacenter
   - Make sure the `ssh_key_name` matches your key name in Hetzner

3. Make the run script executable:

```bash
chmod +x setup.sh
```

4. Run the deployment script:

```bash
./setup.sh
```

## What this does

1. Creates a CX22 server on Hetzner Cloud
2. Installs K3s (lightweight Kubernetes)
3. Retrieves the kubeconfig and saves it locally
4. Verifies the installation
5. Checks and installs Helm if not already present on your local machine

## Tools Installed

- **K3s**: A lightweight Kubernetes distribution perfect for edge and development environments
- **Helm**: The package manager for Kubernetes, which will be installed on your local machine if not already present

## Using your K3s cluster

After successful deployment, set your KUBECONFIG environment variable to use kubectl:

```bash
export KUBECONFIG=$(pwd)/../k3s-kubeconfig.yaml
kubectl get nodes
```

### Using Helm with your cluster

Once the setup is complete, you can use Helm to install applications on your K3s cluster:

```bash
# Add a Helm repository
helm repo add bitnami https://charts.bitnami.com/bitnami

# Install an application (e.g., Nginx)
helm install my-nginx bitnami/nginx
```

## Cleanup

To delete the server when you're done, you can use the Hetzner Cloud console or API.

Using curl:
```bash
curl -X DELETE \
  -H "Authorization: Bearer $HETZNER_API_TOKEN" \
  https://api.hetzner.cloud/v1/servers/{server_id}
```

Replace `{server_id}` with the ID of your server, which is displayed during the playbook execution.