# on a fresh Jenkins VM run this command to make docker start on boot
sudo systemctl enable docker

# run this command to start docker now
sudo systemctl start docker

# start MySQL
docker run -p 3306:3306 --name mysql-1 -e MYSQL_ROOT_PASSWORD=default -d mysql:latest

# start PostgreSQL
docker run --name my-postgres -e POSTGRES_PASSWORD=default -p 5432:5432 -d postgres

# install python libs for PostgreSQL
pip install psycopg2 records
