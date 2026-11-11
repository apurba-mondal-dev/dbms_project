from rapidfuzz import fuzz
from fetch_data import fetch_students

def calculate_similarity(s1, s2):

    return fuzz.ratio(
        str(s1).lower().strip(),
        str(s2).lower().strip()
    )


def detect_duplicates():

    df = fetch_students()

    duplicates = []

    for i in range(len(df)):

        for j in range(i + 1, len(df)):

            s1 = df.iloc[i]
            s2 = df.iloc[j]

            name_score = calculate_similarity(
                s1["STUDENT_NAME"],
                s2["STUDENT_NAME"]
            )

            email_score = calculate_similarity(
                s1["EMAIL"],
                s2["EMAIL"]
            )

            phone_score = calculate_similarity(
                s1["PHONE"],
                s2["PHONE"]
            )

            final_score = (
                0.50 * name_score +
                0.30 * email_score +
                0.20 * phone_score
            )

            if final_score >= 75:

                duplicates.append({
                    "ID 1": s1["STUDENT_ID"],
                    "Name 1": s1["STUDENT_NAME"],
                    "ID 2": s2["STUDENT_ID"],
                    "Name 2": s2["STUDENT_NAME"],
                    "Similarity": round(final_score, 2)
                })

    return duplicates


if __name__ == "__main__":

    results = detect_duplicates()

    for result in results:
        print(result)