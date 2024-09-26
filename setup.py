# sql setup for taskmanger.py
import mysql.connector as sql
pword = input("Enter mysql password: ")
con = sql.connect(user = "root", host = "localhost", passwd = f"{pword}")
cursor = con.cursor()

# create db
cursor.execute("CREATE DATABASE taskmanager")
cursor.execute("USE taskmanager")
print("Database created.")

# create "tasks" table
q = "CREATE TABLE tasks( username varchar(30), task varchar(100), status varchar(30))"
cursor.execute(q)
con.commit()
print("Tasks table created.")

# create "userinfo" table
q = """create table userinfo(
    username varchar(30),
    password varchar(30),
    name varchar(30),
    age int(2),
    address varchar(100))"""
cursor.execute(q)
con.commit()
print("Userinfo table created.")
print("Setup complete.")
