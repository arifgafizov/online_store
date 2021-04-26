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

```bash
docker run -d --name web-store --network="local-apps" -p 8000:8000 -v ~/online_store:/web_django web-django
```

```bash
docker run --rm --network="local-apps" -v ~/online_store:/web_django \
  web-django python3 ./manage.py migrate
```

```bash
docker run --rm --network="local-apps" -v ~/online_store:/web_django \
  web-django python3 ./manage.py collectstatic
```

```bash
docker run --name nginx-1.20 \
    -v /root/online_store/nginx/conf/nginx.conf:/etc/nginx/conf.d/default.conf \
    -v /root/online_store/static/:/opt/static/ \
    -v /root/front_for_web_shop/dist/spa:/opt/spa \
    -p 80:80 \
    --network="local-apps" \
    --restart always \
    -d nginx:1.20.0-alpine
```

```bash
docker run -it --rm \
    -v /root/front_for_web_shop/:/front_for_web_shop/ \
    node bash
```

```bash
docker-compose up -d
```
