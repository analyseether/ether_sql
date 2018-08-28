createdb ether_sql_tests
sudo -u postgres psql -U travis -d postgres -c "alter user travis with password 'develop';"
