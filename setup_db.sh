#!/bin/bash

echo "🗃️ Setting up MariaDB database 'robertodb'..."

# Prompt for MariaDB root password
read -sp "Enter MariaDB root password: " dbpass
echo ""

# Create the database if it doesn't exist
mysql -u root -p"$dbpass" -e "CREATE DATABASE IF NOT EXISTS robertodb;"

# Import the SQL file
mysql -u root -p"$dbpass" robertodb < db/robertodb.sql

echo "✅ Database 'robertodb' has been set up successfully."
