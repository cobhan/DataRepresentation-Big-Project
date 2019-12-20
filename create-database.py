import mysql.connector
import dbconfig as cfg

db = mysql.connector.connect(
	host=cfg.mysql['host'],
	user=cfg.mysql['user'],
	password=cfg.mysql['password'],
)

cursor = db.cursor()
sql="CREATE DATABASE phil"
cursor.execute(sql)