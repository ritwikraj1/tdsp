# Create Database and Import Data through pgRouting
User 'postgres' and database 'postgres' are created by default when installing pgRouting. But it is recommended to create another user and to create separate databases for different cities, to work in the psql environment.

## Steps to create database and import data through pgRouting is following:
1) First, change the password of user 'postgres' to 'postgres'. To do that, open the terminal window and enter:
```
sudo -u postgres psql
```

2) It will open the psql environment. While there, enter:
```
ALTER USER postgres PASSWORD 'postgres';
\q
```

3) Make a backup of your pg_hba.conf file. To do that, open the terminal and enter:
```
cd /etc/postgresql/9.5/main
sudo cp pg_hba.conf pg_hba.conf.bak
```

4) Open the pg_hba.conf file on terminal:
```
sudo nano /etc/postgresql/9.5/main/pg_hba.conf
```

5) Change authentication method for postgres to 'md5' and for 'all' to 'trust'. It will remove password requirement from all the users except postgres. Also, comment out the credentials related to IPv4 and IPv6, and use a common connection for them, with address 'localhost' and method 'trust'. Final file looks like:
```
# Database administrative login by Unix domain socket
local   all             postgres                                md5

# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     trust
host    all             all             localhost               trust
# IPv4 local connections:
#host    all             all             127.0.0.1/32            md5
# IPv6 local connections:
#host    all             all             ::1/128                 md5
# Allow replication connections from localhost, by a user with the
# replication privilege.
#local   replication     postgres                                peer
#host    replication     postgres        127.0.0.1/32            md5
#host    replication     postgres        ::1/128                 md5
```
More information about pg_hba.conf on: https://www.postgresql.org/docs/9.1/static/auth-pg-hba-conf.html

6) Restart postgresql:
```
sudo service postgresql restart
```

7) Log in to the database 'postgres':
```
psql -U postgres
Input password: "postgres"
```

8) Create a user 'user' inside the psql environment. The role of 'user' is a superuser:
```
CREATE ROLE "user" SUPERUSER LOGIN;
\q
```

At this point, a role named "user" is created, but there is no Database named "user". So, when we write "psql -U user", it tries to connect to DB "user" (which doesn't exist) through role "user". Instead of doing this, write "psql -U user postgres". It will connect to DB "postgres" through role "user".

9) Install the osm2pgrouting tool. While on terminal:
```
sudo apt-add-repository -y ppa:georepublic/pgrouting
sudo apt-get update
sudo apt-get install osm2pgrouting
```

### Steps 1 - 9 is a one-time process that we do when we first install pgRouting, and are setting up the psql for use. The don't need to be performed everytime we are creating the database for a new city. The steps that follow, need to be performed everytime we create the database of a new city.

10) While on termnal, log in to the 'postgres' database as user 'user':
```
psql -U user postgres
```

11) Create a database for the city. Here, we are naming the database 'buffalo_routing' for Buffalo:
```
CREATE DATABASE buffalo_routing;
```

12) Change the log in from database 'postgres' to database 'buffalo_routing':
```
\c buffalo_routing
```

13) Create necessary extensions for 'buffalo_routing' DB and then, exit:
```
CREATE EXTENSION postgis;
CREATE EXTENSION pgrouting;
\q
```

14) Go back to terminal, and if there isn't a directory, make one:
```
mkdir ~/Desktop/workshop
```

15) Change the directory to workshop directory:
```
cd ~/Desktop/workshop
```

16) Provide the name and the bounding box of the city you are working with. While inside the workshop directory, issue the following commands:
```
CITY="BUFFALO_US"
BBOX="-78.9086,42.7858,-78.6388,43.0197"
```

17) Import the data in the workshop directory:
```
wget --progress=dot:mega -O "$CITY.osm" "http://www.overpass-api.de/api/xapi?*[bbox=${BBOX}][@meta]"
```

18) Convert the OSM data to pgRouting data. While inside the workshop directory, run the converter:
```
osm2pgrouting     -f BUFFALO_US.osm     -d buffalo_routing     -U user
```

And you are done! To check if the tables have been created:
```
psql -U user -d buffalo_routing -c "\d"
```
