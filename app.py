import streamlit as st
import pandas as pd

from fetch_data import fetch_students
from duplicate_detection import detect_duplicates
from save_results import save_duplicates

st.set_page_config(
    page_title="Duplicate Record Detection",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Intelligent Duplicate Record Detection System")

st.write(
    "An AI-powered system for identifying "
    "duplicate student records."
)

if st.button("View Student Records"):

    df = fetch_students()

    st.subheader("Student Database")
    st.dataframe(df, use_container_width=True)

if st.button("Detect Duplicates"):

    results = detect_duplicates()

    if results:

        st.subheader("Detected Duplicate Records")

        result_df = pd.DataFrame(results)

        st.dataframe(
            result_df,
            use_container_width=True
        )

        st.metric(
            "Potential Duplicate Pairs",
            len(results)
        )

    else:
        st.success("No duplicate records found!")