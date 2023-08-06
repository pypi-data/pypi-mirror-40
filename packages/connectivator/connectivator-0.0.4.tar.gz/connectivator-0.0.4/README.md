## Connectivator

Set of wrapper functions for reading data from a Redshift/postgres database and writing contents to a CSV or Google sheet.

### Current State

* Connect to Postgres / Redshift: `postgres.get_engine`
* Read output of a sql query into a data frame: `transfer.read_sql_data`
* Write output of SQL files to CSV: `transfer.sqls_to_csv`
* Read contents of a Google sheet into a data frame: `gsheets.get_ws_data`
* Update contents of a Google sheet using a data frame: `gsheets.update_ws`

### Environment Variables

* Add a `.env` file to the project root directory.
* Add the following environment variables, replacing with values relevant for your connections. Format:

**Postgres/Redshift Connection**

```
export PGHOST = instance-name.abc123.us-east-1.redshift.amazonaws.com
export PGPORT = 5439
export PGUSER = your_user_name
export PGPASSWORD = your_password
```

* Load the environment variables before running the script. For example, by running `source .env` in the terminal you are using to run Python scripts.
