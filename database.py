import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

local_dsn = "tcps://db.freesql.com:2484/26ai_un3c1"
connection = oracledb.connect(
    user="APURBA_MONDAL2024_SCHEMA_994AL",
    password="8SDR8$7DcMR0TFQB6YBAJ06RXU2SA8",
    dsn=local_dsn)

print("Successfully connected to Oracle Database")

cursor = connection.cursor()
for result in cursor.execute("SELECT * FROM DUAL"):
    print(result)

def get_connection():
    connection = oracledb.connect(
        user="APURBA_MONDAL2024_SCHEMA_994AL",
        password="8SDR8$7DcMR0TFQB6YBAJ06RXU2SA8",
        dsn=local_dsn
    )

    return connection