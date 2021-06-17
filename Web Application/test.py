import sqlite3
conn = sqlite3.connect('federatedhealth.db')
cursor = conn.execute("INSERT INTO users (uname,username,password) VALUES('Maneesh','mnsh','mnsh@123'")
conn.commit()
conn.close()
conn = sqlite3.connect('federatedhealth.db')
cursor = conn.execute("SELECT * from users")
for row in cursor:
    print(row[0],row[1],row[2],row[3])
conn.close()