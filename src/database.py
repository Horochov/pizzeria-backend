import psycopg2

connection = psycopg2.connect(dbname="restaurant", user="postgres", password="postgres")
cursor = connection.cursor()

cursor.execute("""SELECT * FROM restaurant_schema.employees""")
xd = cursor.fetchall()
print(xd)

connection.commit()
cursor.close()
connection.close()
