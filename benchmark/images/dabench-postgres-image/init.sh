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