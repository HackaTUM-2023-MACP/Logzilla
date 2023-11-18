# Flask backend

## Database

The database runs in a docker container built from the ankane/pgvector image. It comes with the pgvector extension preinstalled. To create the docker container and initialize the table(s), cd into the db folder and run the `init_db.sh` bash script:

```bash
POSTGRES_PASSWORD="some_safe_password" bash init_db.sh
```

This will create an unpopulated table normally under the postgres db and username. To populate the table, use `populate_db.py` (or functions therein). For example:

```bash
python3 populate_db.py ./logs/test_log1.out --user "postgres" --password "hello"
```
