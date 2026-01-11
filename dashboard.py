import streamlit as st
from database import cursor

# =========================================================
# DASHBOARD PAGE
# =========================================================
def dashboard_page():

    st.title(f"Hello, {st.session_state.user_name} 👋")

    # =====================================================
    # LOAD USER PROFILE
    # =====================================================
    cursor.execute("""
        SELECT role, grade, time, strong_subjects, weak_subjects, teaches
        FROM profiles
        WHERE user_id = ?
    """, (st.session_state.user_id,))
    
    profile = cursor.fetchone()

    if not profile:
        st.warning("Please complete your profile in Matchmaking first.")
        return

    role, grade, time, strong, weak, teaches = profile

    subjects = (
        teaches if role == "Teacher"
        else strong if strong
        else weak
    )

    # =====================================================
    # PROFILE CARD
    # =====================================================
    st.subheader("Your Details")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Role:**", role)
        st.write("**Grade:**", grade)
        st.write("**Time Slot:**", time)

    with col2:
        st.write("**Subjects:**")
        st.write(subjects.replace(",", ", ") if subjects else "—")

    st.divider()

    # =====================================================
    # STATS
    # =====================================================
    cursor.execute("""
        SELECT COUNT(DISTINCT mentor), AVG(rating)
        FROM ratings
        WHERE mentor = ?
    """, (st.session_state.user_name,))

    worked_with, avg_rating = cursor.fetchone()
    worked_with = worked_with or 0
    avg_rating = round(avg_rating, 2) if avg_rating else "—"

    # Temporary logic (can improve later)
    streak = 5
    leaderboard_position = 12

    st.subheader("Your Progress")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🔥 Streak", f"{streak} days")
    c2.metric("🏆 Leaderboard", f"#{leaderboard_position}")
    c3.metric("🤝 Worked With", worked_with)
    c4.metric("⭐ Avg Rating", avg_rating)

    st.divider()

    # =====================================================
    # HISTORY
    # =====================================================
    st.subheader("Session History")

    cursor.execute("""
        SELECT mentor, rating
        FROM ratings
        WHERE mentor = ?
        ORDER BY rowid DESC
        LIMIT 10
    """, (st.session_state.user_name,))

    rows = cursor.fetchall()

    if rows:
        history = []
        for r in rows:
            history.append({
                "Mentor": r[0],
                "Rating": r[1]
            })

        st.table(history)
    else:
        st.info("No session history yet.")
