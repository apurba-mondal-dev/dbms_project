import pandas as pd
from database import get_connection

def fetch_students():

    conn = get_connection()

    query = """
        SELECT STUDENT_ID, STUDENT_NAME,
               EMAIL, PHONE, DEPARTMENT, CITY
        FROM STUDENTS
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


if __name__ == "__main__":
    students = fetch_students()

    print(students)