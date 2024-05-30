#!/bin/bash

# Define a function to execute a command and check the return value
execute_command() {
    "$@"
    local status=$?
    if [ $status -ne 0 ]; then
        echo "Command execution failed: $1"
        return 1
    fi
}

# Array of commands
commands=("apt update" "pip install --upgrade pip" "apt install -y postgresql")

# Loop to execute commands until all are successful
for cmd in "${commands[@]}"; do
    while true; do
        execute_command $cmd && break
    done
done



service postgresql start

su - postgres <<EOF
psql -c "CREATE USER dabench WITH PASSWORD '123456';"
psql -c "CREATE DATABASE dadb;"
psql -c "ALTER DATABASE dadb OWNER TO dabench;"
EOF

echo "listen_addresses = 'localhost'" >> /etc/postgresql/15/main/postgresql.conf
echo "listen_addresses = '*'" >> /etc/postgresql/15/main/postgresql.conf
touch ~/.pgpass
chmod 600 ~/.pgpass
echo "localhost:5432:dadb:dabench:123456" >> ~/.pgpass
echo 'host    all             all             0.0.0.0/0               md5' >> /etc/postgresql/15/main/pg_hba.conf

echo 'service postgresql restart' >> ~/.bashrc
service postgresql restart

cd /workspace

pip install google-cloud-bigquery db-dtypes pandas
pip install snowflake-connector-python
pip install google-cloud-bigquery db-dtypes pandas matplotlib \
    scikit-learn seaborn numpy scipy statsmodels xgboost plotly tabulate
