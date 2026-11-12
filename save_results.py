from database import get_connection
from duplicate_detection import detect_duplicates

def save_duplicates():

    conn = get_connection()
    cursor = conn.cursor()

    results = detect_duplicates()

    for index, item in enumerate(results, start=1):

        cursor.execute("""
            INSERT INTO DUPLICATE_RECORDS
            (
                MATCH_ID,
                STUDENT_ID_1,
                STUDENT_ID_2,
                SIMILARITY_SCORE,
                STATUS
            )
            VALUES (:1, :2, :3, :4, 'PENDING')
        """, (
            index,
            int(item["ID 1"]),
            int(item["ID 2"]),
            float(item["Similarity"])
        ))

    conn.commit()

    cursor.close()
    conn.close()

    print("Duplicate records saved successfully!")


if __name__ == "__main__":
    save_duplicates()