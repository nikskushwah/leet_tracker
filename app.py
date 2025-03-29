# app.py
import time
import streamlit as st
import pandas as pd
from datetime import datetime
from auth import login_form, register_form, logout_action
from database import get_db_connection
from operations import find_ques
from spaced_repetition import spaced_repetition_view

DB_CONFIG = st.secrets["db_config"]

# Load CSS styling
# st.markdown(get_css(), unsafe_allow_html=True)

def run_app():
    topics = ["Array", "String", "Hash Table", "Dynamic Programming", "Math", "Sorting", "Greedy", "Depth-First Search",
              "Binary Search", "Database", "Matrix", "Breadth-First Search", "Tree", "Bit Manipulation", "Two Pointers",
              "Prefix Sum", "Heap (Priority Queue)", "Binary Tree", "Simulation", "Stack", "Graph", "Counting",
              "Sliding Window", "Design", "Enumeration", "Backtracking", "Union Find", "Linked List", "Number Theory",
              "Ordered Set", "Monotonic Stack", "Segment Tree", "Trie", "Combinatorics", "Bitmask", "Queue",
              "Recursion", "Divide and Conquer", "Memoization", "Binary Indexed Tree", "Geometry",
              "Binary Search Tree", "Hash Function", "String Matching", "Topological Sort", "Shortest Path",
              "Rolling Hash", "Game Theory", "Interactive", "Data Stream", "Monotonic Queue", "Brainteaser",
              "Randomized", "Merge Sort", "Doubly-Linked List", "Counting Sort", "Iterator", "Concurrency",
              "Probability and Statistics", "Quickselect", "Suffix Array", "Bucket Sort", "Line Sweep",
              "Minimum Spanning Tree", "Shell", "Reservoir Sampling", "Strongly Connected Component",
              "Eulerian Circuit", "Radix Sort", "Rejection Sampling", "Biconnected Component", "Collapse"]

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        st.markdown('<h1 class="header">Leetcode Tracker</h1>', unsafe_allow_html=True)
        st.sidebar.markdown('<h1 class="header" style="text-align: center;">Leetcode Tracker</h1>', unsafe_allow_html=True)
        auth_mode = st.sidebar.radio("Select Mode:", ("Login", "Register"), key="auth_mode")
        if auth_mode == "Login":
            login_form()
        else:
            register_form()
    else:
        st.markdown('<h1 class="header">Leetcode Tracker</h1>', unsafe_allow_html=True)
        st.sidebar.markdown('<h1 class="header" style="text-align: center;">Leetcode Tracker</h1>', unsafe_allow_html=True)
        st.sidebar.markdown(
            f"<p style='text-align: center; color: #ff6f61;'>Logged in as: <strong>{st.session_state['username']}</strong></p>",
            unsafe_allow_html=True
        )
        col1, col2, col3 = st.sidebar.columns([1, 2, 1])
        if col2.button("Logout"):
            logout_action()

        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🗂️ Navigation")
        view = st.sidebar.radio("", ["🚀 Leetcode Tracker", "📝 Edit Question", "⏰ Spaced Repetition Review"], index=0)

        if view == "🚀 Leetcode Tracker":
            st.subheader("Add a Leetcode Question")
            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                number = st.text_input("Leetcode question number:")
                # Create one placeholder to display messages (error or success)
                message_placeholder = st.empty()

            with col2:
                solved_date = st.date_input("Date Solved:", value=datetime.now().date())

            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Enter"):
                    try:
                        conn = get_db_connection()
                        with conn.cursor() as cursor:
                            # Check if question ID already exists for this user
                            cursor.execute(
                                "SELECT * FROM questions WHERE question_id = %s AND user_email = %s",
                                (number, st.session_state["user_email"])
                            )
                            existing = cursor.fetchone()

                        if existing:
                            # Use the same placeholder to show error message
                            message_placeholder.error("Question already exists in your database!")
                            conn.close()
                        else:
                            # If not existing, insert the question
                            slug, description, extra = find_ques(int(number))
                            next_review_date = datetime.now().date() + pd.Timedelta(days=2)
                            with conn.cursor() as cursor:
                                cursor.execute("""
                                    INSERT INTO questions (question_id, slug, description, extra, date, user_email, next_review_date)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                                """, (number, slug, description, extra, solved_date, st.session_state["user_email"], next_review_date))
                            conn.commit()
                            conn.close()
                            # Display success message in the same placeholder
                            message_placeholder.success("Question inserted into the database!")
                            time.sleep(3)
                            message_placeholder.empty()
                    except Exception as e:
                        message_placeholder.error(f"Error: {e}")

            conn = get_db_connection()
            query = "SELECT * FROM questions WHERE user_email = %s"
            df = pd.read_sql(query, conn, params=(st.session_state["user_email"],))
            conn.close()

            if not df.empty:
                display_df = df[['question_id', 'slug', 'description', 'extra', 'date']].rename(columns={
                    'question_id': 'Question ID',
                    'slug': 'Question Link',
                    'description': 'Description',
                    'extra': 'Topics',
                    'date': 'Date'
                })
                display_df["Question Link"] = display_df["Question Link"].apply(
                    lambda s: f"https://leetcode.com/problems/{s}/description/"
                )
                st.markdown("### Questions")
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    filter_qid = st.text_input("Filter by Question ID", "")
                with col2:
                    filter_qlink = st.text_input("Filter by Link (slug)", "")
                unique_desc = ["All"] + sorted(display_df["Description"].dropna().unique().tolist())
                with col3:
                    filter_desc = st.selectbox("Filter by Description", unique_desc)
                with col4:
                    filter_topics = st.selectbox("Filter by Topics", ["All"] + topics)
                with col5:
                    filter_date = st.text_input("Filter by Date (YYYY-MM-DD)", "")

                filtered_df = display_df.copy()
                if filter_qid:
                    filtered_df = filtered_df[filtered_df["Question ID"].astype(str).str.contains(filter_qid)]
                if filter_qlink:
                    filtered_df = filtered_df[filtered_df["Question Link"].str.contains(filter_qlink)]
                if filter_desc and filter_desc != "All":
                    filtered_df = filtered_df[filtered_df["Description"] == filter_desc]
                if filter_topics and filter_topics != "All":
                    filtered_df = filtered_df[filtered_df["Topics"].apply(
                        lambda x: filter_topics.strip() in [t.strip() for t in x.split(",")]
                    )]
                if filter_date:
                    filtered_df = filtered_df[filtered_df["Date"].astype(str).str.contains(filter_date)]

                filtered_df["Date"] = pd.to_datetime(filtered_df["Date"])
                col_config = {
                    "Question Link": st.column_config.LinkColumn(
                        "Question Link",
                        help="Click to open the Leetcode problem",
                        validate=r"^https://leetcode\.com/problems/.*?/description/$",
                        max_chars=100,
                        display_text=r"https://leetcode\.com/problems/(.*?)/description/"
                    ),
                    "Date": st.column_config.DateColumn(
                        "Date",
                        help="Date added",
                        format="YYYY-MM-DD"
                    )
                }
                st.data_editor(filtered_df, column_config=col_config, disabled=True, hide_index=True)
            else:
                st.info("No questions added yet.")
        
        elif view == "📝 Edit Question":
            st.subheader("Edit a Question")
            conn = get_db_connection()
            query = "SELECT * FROM questions WHERE user_email = %s"
            df = pd.read_sql(query, conn, params=(st.session_state["user_email"],))
            conn.close()

            if not df.empty:
                edit_id = st.selectbox(
                    "Select a question to edit",
                    options=df["id"].tolist(),
                    format_func=lambda id: f"Q{df.loc[df['id'] == id, 'question_id'].iloc[0]}: {df.loc[df['id'] == id, 'description'].iloc[0][:30]}..."
                )
                record = df[df["id"] == edit_id].iloc[0]
                new_question_number = st.text_input("Leetcode question number", value=record["question_id"])
                new_description = st.text_area("Description", value=record["description"])
                new_topics = st.text_input("Topics", value=record["extra"])
                new_date = st.date_input("Date", value=record["date"])
                if st.button("Update"):
                    try:
                        conn = get_db_connection()
                        with conn.cursor() as cursor:
                            cursor.execute("""
                                UPDATE questions
                                SET question_id = %s, description = %s, extra = %s, date = %s
                                WHERE id = %s;
                            """, (new_question_number, new_description, new_topics, new_date, edit_id))
                        conn.commit()
                        conn.close()
                        st.success("Record updated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error updating record: {e}")
            else:
                st.info("No questions added yet.")

        elif view == "⏰ Spaced Repetition Review":
            spaced_repetition_view(st.session_state["user_email"])

if __name__ == "__main__":
    run_app()
