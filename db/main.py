from mysql.connector import (connection)

cnx = connection.MySQLConnection(user="root", password="VicDep12", host="vichogent.be:40068", database="database1")

cnx.close()