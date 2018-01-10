# download mysql-connector-python-2.1.7.tar.gz from
# https://dev.mysql.com/downloads/connector/python/
# or
# https://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-2.1.7.tar.gz
# will need to create free account or login to your existing account

'''
scp -P 2222 /Users/dmitrytokarev/Downloads/mysql-connector-python-2.1.7.tar.gz default@localhost:/home/default/
ssh -p 2222 default@localhost
python -m venv venv
tar xzf mysql-connector-python-2.1.7.tar.gz
cd mysql-connector-python-2.1.7
../venv/bin/python setup.py install
cd ../venv/
# bin/pip install mysql-connector-python  # Oracle seem now distribute on PyPI - beta version as of 2017/11/20
bin/python
'''

import mysql
import mysql.connector

cnx = mysql.connector.connect(user='root', password='default', host='127.0.0.1')
cnx.cmd_query('create database test;')
cnx.connect(database='test')

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
cursor = cnx.cursor()
cursor.execute(s2)
cursor.execute(s3)
r = cursor.fetchall()
assert r == [(123456, 'Tokarev', 'Dmitry', 'USA', 'Seattle')]
