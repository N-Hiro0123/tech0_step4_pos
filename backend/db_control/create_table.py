import os

# Obtain the absolute path of the SSL certificate
base_path = os.path.dirname(os.path.abspath(__file__))
ssl_cert_path = os.path.join(base_path, 'DigiCertGlobalRootG2.crt.pem')


from dotenv import load_dotenv

load_dotenv()

AZURE_MY_SERVER = os.getenv("AZURE_MY_SERVER")
AZURE_MY_ADMIN = os.getenv("AZURE_MY_ADMIN")
AZURE_MY_PASSWORD = os.getenv("AZURE_MY_PASSWORD")
AZURE_MY_DATABASE = os.getenv("AZURE_MY_DATABASE")
AZURE_SSL_CA = ssl_cert_path  # create_table.pyと同じ場所におく

import mysql.connector
from mysql.connector import errorcode

# Obtain connection string information from the portal

config = {
    'host': AZURE_MY_SERVER + '.mysql.database.azure.com',
    'user': AZURE_MY_ADMIN,
    'password': AZURE_MY_PASSWORD,
    'database': AZURE_MY_DATABASE,
    'client_flags': [mysql.connector.ClientFlag.SSL],
    'ssl_ca': AZURE_SSL_CA,
}

# Construct connection string

try:
    conn = mysql.connector.connect(**config)
    print("Connection established")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with the user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor = conn.cursor()

    # Drop previous table of same name if one exists
    cursor.execute("DROP TABLE IF EXISTS inventory;")
    print("Finished dropping table (if existed).")

    # Create table
    cursor.execute("CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
    print("Finished creating table.")

    # Insert some data into table
    cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("banana", 150))
    print("Inserted", cursor.rowcount, "row(s) of data.")
    cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("orange", 154))
    print("Inserted", cursor.rowcount, "row(s) of data.")
    cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("apple", 100))
    print("Inserted", cursor.rowcount, "row(s) of data.")

    # Cleanup
    conn.commit()
    cursor.close()
    conn.close()
    print("Done.")
