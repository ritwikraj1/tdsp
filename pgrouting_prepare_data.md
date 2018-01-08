# Create Database and Import Data through pgRouting

## Steps to create database and import data through pgRouting is following:
1) User 'postgres' is created by default when installing pgRouting. First, change its password to 'postgres'. To do that, open the terminal window and enter:
```
sudo -u postgres psql
```

2) It will open the psql environment. While there, enter:
```
ALTER USER postgres PASSWORD 'postgres';
\q
```
3)  Make a backup of your pg_hba.conf file. To do that, open the terminal and enter:
```
cd /etc/postgresql/9.5/main
sudo cp pg_hba.conf pg_hba.conf.bak
```
