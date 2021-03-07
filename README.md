```bash
docker network create local-apps
```

```bash
docker run --name local-pg13 \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_INITDB_ARGS="--locale=C.UTF-8" \
    -v ~/Documents/storedata/pg-data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network="local-apps" \
    --restart always \
    -d postgres:13.2-alpine
```

```bash
docker exec -it local-pg13 psql -U postgres
```

```sql
CREATE USER online_store CREATEDB LOGIN PASSWORD 'super_mega_store_password';
CREATE DATABASE online_store WITH OWNER = online_store CONNECTION LIMIT = -1;
GRANT ALL PRIVILEGES ON DATABASE online_store to online_store;
```