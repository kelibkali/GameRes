from peewee import MySQLDatabase
from config.settings import (db_name,db_user,db_password,db_host,db_port)

db_inst = MySQLDatabase(db_name,user=db_user,password=db_password,host=db_host,port=db_port)