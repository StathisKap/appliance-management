# Appliance Management System

### **TL:DR**

|user| passowrd|
|-|-|
|`admin`| `admin`|

|Deployment| Location|
|-|-|
|Local |`python manage.py runserver`|
|Kubernetes Deployment| https://appliance-management.co.uk|
|Heroku Deployment | https://appliance-management-9e691367f1f8.herokuapp.com |

There is an `.env` file so the local deployment will still connect to postgres

## Overview

![https://cdn.appliance-management.co.uk/app-manager-public/appliance-management-2x.gif](https://cdn.appliance-management.co.uk/app-manager-public/appliance-management.gif?)


## Architecture

There are 2 ways in which this app is now publicly deployed.

1. On Kubernetes on a small server by [Hetzner.com](https://www.hetzner.com/), alongside all of its dependencies (PG, MinIO, CertManager) - €3.95/mo
1. On Heroku with Postgres - At most $12/mo

![(https://cdn.appliance-management.co.uk/app-manager-public/appliance-management.jpg](https://cdn.appliance-management.co.uk/app-manager-public/appliance-management.jpg?)

## Kubernetes

The Kubernetes deployment starts off by using the ansible notebook at `k3s/setup/hetzner_k3s.yaml`. That sets up the cluster.
A script is provided that will make sure all dependenices are installed first and install `cert-manager` thereafter, so that we can get https with the green lock. (SSL certificates)

Then, we go to `k3s/www` and setup Postgres and MinIO first using the README files.

Then, we setup `k3s/www/django-app`

For the `django-app` to store items on the CDN ( MinIO ), we first need to create an API key.

Credetials for MinIO will be `admin` and `password123`.
Credetials for PG will be `postgres` and `gZRiEt9FuCLgo85`.


That's it!!

If you want to update the deployment, then you'll need to:
1. Create a github repo
2. Add your Docker credentials and Kubeconfig as secrets
3. Edit the `.github/workflows/deploy.yaml` file with your own image tag
4. Make a commit.

The new image will be rebuilt and the app will be updated

## Heroku

Go to your Heroku account, hook up your github repo and it should work fine.
