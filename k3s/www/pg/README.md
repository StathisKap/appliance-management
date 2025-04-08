# Bitnami Postgres

```bash
helm upgrade my-postgres oci://registry-1.docker.io/bitnamicharts/postgresql --install --create-namespace -n postgres -f values.yaml
psql 'postgres://postgres:gZRiEt9FuCLgo85@159.69.25.234:5432'
```

A DNS record has also been set up for this server, so you can also access the PG using
```bash
psql 'postgres://postgres:gZRiEt9FuCLgo85@tcp.appliance-management.co.uk:5432'
```