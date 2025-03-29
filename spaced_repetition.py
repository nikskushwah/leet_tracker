import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime

DB_CONFIG = st.secrets["db_config"]


# Database connection utility
def get_db_connection():
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        port=DB_CONFIG["port"]
    )

# SM-2 spaced repetition algorithm
def update_review_schedule(question, remembered):
    conn = get_db_connection()

    repetition_count = question['repetition_count']
    review_interval = question['review_interval']
    ease_factor = question['ease_factor']

    if remembered:
        if repetition_count == 0:
            review_interval = 2  # changed from 1 day to 2 days
        elif repetition_count == 1:
            review_interval = 6
        else:
            review_interval = int(round(review_interval * ease_factor))

        repetition_count += 1
        ease_factor = min(max(ease_factor + 0.1, 1.3), 2.5)
    else:
        repetition_count = 0
        review_interval = 2  # changed from 1 day to 2 days
        ease_factor = max(ease_factor - 0.2, 1.3)

    next_review_date = datetime.now().date() + pd.Timedelta(days=review_interval)

    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE questions
            SET repetition_count=%s, review_interval=%s, ease_factor=%s, next_review_date=%s
            WHERE id=%s;
        """, (repetition_count, review_interval, ease_factor, next_review_date, question['id']))
    conn.commit()
    conn.close()


# Main spaced repetition view
def spaced_repetition_view(user_email):
    st.header("📅 Spaced Repetition Review")

    today = datetime.now().date()

    conn = get_db_connection()
    query = """
        SELECT * FROM questions
        WHERE user_email = %s AND next_review_date <= %s
        ORDER BY next_review_date ASC
    """
    due_df = pd.read_sql(query, conn, params=(user_email, today))
    conn.close()

    if due_df.empty:
        st.info("🎉 No questions are due for review today!")
    else:
        for idx, row in due_df.iterrows():
            with st.expander(f"Q{row['question_id']}: {row['description'][:60]}..."):
                st.markdown(f"**Question Link:** [Leetcode Problem](https://leetcode.com/problems/{row['slug']}/description/)")
                st.markdown(f"**Description:** {row['description']}")
                st.markdown(f"**Topics:** {row['extra']}")
                st.markdown(f"**Review Count:** {row['repetition_count']}")
                st.markdown(f"**Review Interval:** {row['review_interval']} days")
                st.markdown(f"**Ease Factor:** {row['ease_factor']:.2f}")
                st.markdown(f"**Next Review Date:** {row['next_review_date']}")

                col_remember, col_forgot = st.columns(2)
                with col_remember:
                    if st.button(f"✅ Remembered - {row['id']}"):
                        update_review_schedule(row, remembered=True)
                        st.rerun()
                with col_forgot:
                    if st.button(f"❌ Forgot - {row['id']}"):
                        update_review_schedule(row, remembered=False)
                        st.rerun()
