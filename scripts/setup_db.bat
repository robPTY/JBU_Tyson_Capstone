@echo off
setlocal

echo Setting up MariaDB database "robertodb"...

:: Prompt for MariaDB root password
set /p DBPASS=Enter MariaDB root password: 

:: Create the database if it doesn't exist
mysql -u root -p%DBPASS% -e "CREATE DATABASE IF NOT EXISTS robertodb;"

:: Import the SQL dump
mysql -u root -p%DBPASS% robertodb < db\robertodb.sql

echo Done! The database "robertodb" has been set up.
pause
