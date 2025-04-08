# Minio

```bash
helm upgrade my-minio oci://registry-1.docker.io/bitnamicharts/minio --install --create-namespace -n minio -f values.yaml
```

This will create the minio service with the domain name specified in the values.yaml