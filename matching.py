# matching.py

"""
Peer matching logic for Adaptive Learning NGO
"""

# Sample in-memory data (can be replaced with DB later)
PEERS = [
    {"name": "Aarav", "grade": "10", "subject": "Maths"},
    {"name": "Diya", "grade": "10", "subject": "Science"},
    {"name": "Kabir", "grade": "9", "subject": "Maths"},
    {"name": "Ananya", "grade": "11", "subject": "English"},
    {"name": "Riya", "grade": "12", "subject": "Science"},
]


# -------------------------------------------------
# CORE MATCHING FUNCTION (original logic)
# -------------------------------------------------
def match_peers(grade, subject):
    """
    Matches peers based on grade and subject
    """
    matches = []

    for peer in PEERS:
        if peer["grade"] == grade and peer["subject"] == subject:
            matches.append(peer)

    return matches


# -------------------------------------------------
# STREAMLIT-COMPATIBLE WRAPPER (IMPORTANT)
# -------------------------------------------------
def get_peer_matches(grade, subject):
    """
    Wrapper used by Streamlit app
    Prevents ImportError and standardizes output
    """
    return match_peers(grade, subject)
