import records

db_type = 'postgres'
username = 'postgres'
password = 'default'
hostname = 'localhost'
db_name = 'postgres'
port = 5432  # default port 5432
db = records.Database('{db_type}://{user}:{pwd}@{hostname}:{port}/{db_name}'.format(
    db_type=db_type,
    user=username,
    pwd=password,
    hostname=hostname,
    port=port,
    db_name=db_name
))


db.get_table_names()


s1 = '''
CREATE TABLE Persons (
   PersonID int,
   LastName varchar(255),
   FirstName varchar(255),
   Address varchar(255),
   City varchar(255) 
);'''

s2 = "INSERT INTO Persons (PersonID, LastName, FirstName, Address, City) VALUES (123456, 'Tokarev', 'Dmitry', 'USA', 'Seattle');"

r = db.query(s1)
r = db.query(s2)
s3 = "select * from Persons"
r = db.query(s3)  # generator
l = [i for i in r]  # create list
print(l)

familia = l[0]['lastname']
print(familia)


s4 = "INSERT INTO Persons (PersonID, LastName, FirstName, Address, City) VALUES (123456, 'Smith', 'John', 'USA', 'New York');"


# CREATE TABLE "table_name" (users VARCHAR [5],
# "column 2" "data type for column 2" [column 2 constraint(s)],
# ...
# [table constraint(s)] );