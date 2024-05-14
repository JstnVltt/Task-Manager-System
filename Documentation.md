# How to hotfix
Each time a modification has been made to a table, it's necessary to follow these steps:
- go to a terminal and open your database : `sqlite3 instance/test.db` for example.
- drop the tables that have been changed : `DROP TABLE table_name`
- exit sqlite3 : `.exit`
- in the terminal, execute the two following commands : `flask shell` and `db.create_all()`. 
- exit the shell : `exit()`

