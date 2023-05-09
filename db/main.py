from mysql.connector import (connection, errorcode, Error as Mysql_error)

try:
    cnx = connection.MySQLConnection(user="root", password="VicDep12", host="localhost", database="databank1")
    cursor = cnx.cursor()


    query = ("SELECT * FROM airline ")
    cursor.execute(query)

    for (code, name, country) in cursor:
        print(f"{code} {name} {country}")

except Mysql_error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
  cnx.close()