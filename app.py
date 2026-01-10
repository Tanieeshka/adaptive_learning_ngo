import streamlit as st
import google.generativeai as genai
import time
from materials import materials_page
from ratings import show_rating_ui
from matching import find_matches

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(page_title="Sahay - Peer Learning", layout="wide")

# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================
if "stage" not in st.session_state:
    st.session_state.stage = 1

if "profile" not in st.session_state:
    st.session_state.profile = {}

if "mentors" not in st.session_state:
    st.session_state.mentors = []

if "mentees" not in st.session_state:
    st.session_state.mentees = []

if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = {}

if "current_match" not in st.session_state:
    st.session_state.current_match = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

SUBJECTS = ["Mathematics", "English", "Science"]

# =========================================================
# HELPER FUNCTIONS
# =========================================================
def calculate_match_score(mentee, mentor):
    score = 0
    reasons = []
    
    mentee_weak = mentee.get("weak_subjects", [])
    mentor_strong = mentor.get("strong_subjects", mentor.get("teaches", []))
    
    # 1. Skill Match (+50)
    for weak in mentee_weak:
        if weak in mentor_strong:
            score += 50
            reasons.append(f"+50: {weak} help")
    
    # 2. Logistics (+20)
    if mentor["time"] == mentee["time"]:
        score += 20
        reasons.append("+20: same time")
    
    # 3. Peer Match (+10)
    if mentor["grade"] == mentee["grade"]:
        score += 10
        reasons.append("+10: same grade")
    
    return score, reasons

def find_best_mentor(mentee, mentors):
    eligible = [m for m in mentors if m["name"] != mentee["name"]]
    best_mentor, best_score, best_reasons = None, -1, []

    for mentor in eligible:
        score, reasons = calculate_match_score(mentee, mentor)
        if score > best_score:
            best_mentor = mentor
            best_score = score
            best_reasons = reasons

    # Threshold for a "good" match is 15 points
    return best_mentor, best_score, best_reasons if best_score >= 15 else (None, 0, [])

# =========================================================
# APP NAVIGATION
# =========================================================
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Matchmaking", "Learning Materials"])

if page == "Learning Materials":
    materials_page()
    st.stop()  # Stop here if on materials page

# =========================================================
# MAIN APP: MATCHMAKING
# =========================================================
st.title("Sahay: Peer Learning Matchmaking System 🎓")

# ---------------------------------------------------------
# STAGE 1: PROFILE SETUP
# ---------------------------------------------------------
if st.session_state.stage == 1:
    st.header("Step 1: Create Profile")
    
    col1, col2 = st.columns(2)
    with col1:
        role = st.radio("Role", ["Student", "Teacher"])
        name = st.text_input("Full Name")
    with col2:
        grade = st.selectbox("Grade", [f"Grade {i}" for i in range(1, 11)])
        time_slot = st.selectbox("Time Slot", ["4-5 PM", "5-6 PM", "6-7 PM"])

    strong_subjects, weak_subjects, teaches = [], [], []

    if role == "Student":
        c1, c2 = st.columns(2)
        strong_subjects = c1.multiselect("Strong Subjects", SUBJECTS)
        weak_subjects = c2.multiselect("Weak Subjects", SUBJECTS)
    else:
        teaches = st.multiselect("Subjects You Teach", SUBJECTS)

    if st.button("Find Match", type="primary"):
        if not name:
            st.error("Please enter a name")
        else:
            profile = {
                "role": role,
                "name": name,
                "grade": grade,
                "time": time_slot,
                "strong_subjects": strong_subjects,
                "weak_subjects": weak_subjects,
                "teaches": teaches
            }
            
            # Save current user
            st.session_state.profile = profile
            
            # Add to pool (Simulated Database)
            if role == "Student":
                if strong_subjects: st.session_state.mentors.append(profile)
                if weak_subjects: st.session_state.mentees.append(profile)
            else:
                st.session_state.mentors.append(profile)
                
            st.session_state.stage = 2
            st.rerun()

# ---------------------------------------------------------
# STAGE 2: MATCH RESULTS
# ---------------------------------------------------------
elif st.session_state.stage == 2:
    st.header("Step 2: Match Results")
    
    with st.spinner("Finding the perfect mentor..."):
        time.sleep(1.5)
        best_mentor, score, reasons = find_best_mentor(
            st.session_state.profile, 
            st.session_state.mentors
        )

    if best_mentor:
        st.success(f"Match Found! Score: {score}/80")
        st.session_state.current_match = {
            "Mentor": best_mentor["name"],
            "Mentee": st.session_state.profile["name"],
            "Score": score
        }
        
        st.info(f"Why this match? {'; '.join(reasons)}")
        
        if st.button("Start Learning Session"):
            st.session_state.stage = 3
            st.rerun()
    else:
        st.warning("No perfect match found right now.")
        if st.button("Try Again / Edit Profile"):
            st.session_state.stage = 1
            st.rerun()

# ---------------------------------------------------------
# STAGE 3: AI LEARNING SESSION (CHATBOT)
# ---------------------------------------------------------
elif st.session_state.stage == 3:
    st.header("Learning Session 💬")
    
    match = st.session_state.current_match
    st.markdown(f"**Mentor:** {match['Mentor']} | **Mentee:** {match['Mentee']}")

    # --- API SETUP ---
    api_ready = False
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        api_ready = True
    else:
        st.error("⚠️ API Key missing in Secrets. AI will not work.")

    col_chat, col_tools = st.columns([2, 1])

    # --- LEFT: CHAT ---
    with col_chat:
        st.subheader("🤖 AI Tutor")
        
        # Display History
        for role, text in st.session_state.chat_history:
            with st.chat_message(role):
                st.markdown(text)

        # Chat Input
        if api_ready:
            if prompt := st.chat_input("Ask a doubt..."):
                st.session_state.chat_history.append(("user", prompt))
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        try:
                            model = genai.GenerativeModel("gemini-1.5-flash")
                            response = model.generate_content(prompt)
                            st.markdown(response.text)
                            st.session_state.chat_history.append(("assistant", response.text))
                        except Exception as e:
                            st.error(f"Error: {e}")

    # --- RIGHT: TOOLS ---
    with col_tools:
        st.subheader("Tools")
        st.file_uploader("Upload Notes")
        st.divider()
        if st.button("End Session"):
            st.session_state.stage = 4
            st.rerun()

# ---------------------------------------------------------
# STAGE 4: RATING
# ---------------------------------------------------------
elif st.session_state.stage == 4:
    show_rating_ui()
    
    if st.button("Submit & New Session"):
        # Reset Logic
        mentor = st.session_state.current_match["Mentor"]
        points = st.session_state.rating * 10
        st.session_state.leaderboard[mentor] = st.session_state.leaderboard.get(mentor, 0) + points
        
        # Clear specific session states but keep leaderboard/db
        st.session_state.stage = 1
        st.session_state.chat_history = []
        st.session_state.rating = 0
        st.rerun()
