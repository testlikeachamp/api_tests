# download mysql-connector-python-2.1.7.tar.gz from
# https://dev.mysql.com/downloads/connector/python/
# or
# https://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-2.1.7.tar.gz
# will need to create free account or login to your existing account

'''
scp -P 2222 /Users/dmitrytokarev/Downloads/mysql-connector-python-2.1.7.tar.gz default@localhost:/home/default/
ssh -p 2222 default@localhost
python -m venv venv
cd venv/
bin/pip install PyMySQL
bin/python
'''

import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='default',
                             db='test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


# Example from https://github.com/PyMySQL/PyMySQL
create_table = """
CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `email` varchar(255) COLLATE utf8_bin NOT NULL,
    `password` varchar(255) COLLATE utf8_bin NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1 ;
"""
try:
    with connection.cursor() as cursor:
        cursor.execute(create_table)
        # Create a new record
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()


s1 = '''
CREATE TABLE Persons (
   PersonID int,
   LastName varchar(255),
   FirstName varchar(255),
   Address varchar(255),
   City varchar(255) 
);'''
s2 = "INSERT INTO Persons (PersonID, LastName, FirstName, Address, City) VALUES (123456, 'Tokarev', 'Dmitry', 'USA', 'Seattle');"
s3 = "select * from Persons"
with connection.cursor() as cursor:
    cursor.execute(s1)
    cursor.execute(s2)
    cursor.execute(s3)
    r = cursor.fetchall()
    assert r == [{'PersonID': 123456, 'LastName': 'Tokarev', 'FirstName': 'Dmitry', 'Address': 'USA', 'City': 'Seattle'}]




# cnx = mysql.connector.connect(user='root', password='default', host='127.0.0.1')
# cnx.cmd_query('create database test;')
# cnx.connect(database='test')
#
# s1 = '''
# CREATE TABLE Persons (
#    PersonID int,
#    LastName varchar(255),
#    FirstName varchar(255),
#    Address varchar(255),
#    City varchar(255)
# );'''
# s2 = "INSERT INTO Persons (PersonID, LastName, FirstName, Address, City) VALUES (123456, 'Tokarev', 'Dmitry', 'USA', 'Seattle');"
# s3 = "select * from Persons"
# cursor = cnx.cursor()
# cursor.execute(s2)
# cursor.execute(s3)
# r = cursor.fetchall()
# assert r == [(123456, 'Tokarev', 'Dmitry', 'USA', 'Seattle')]
