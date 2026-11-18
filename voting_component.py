import os
import streamlit as st
import sqlite3
from datetime import datetime, timezone
import uuid

os.makedirs("data", exist_ok=True)
DB_PATH = os.path.join("data", "votes.db")

def init_db():
    """Creates the SQLite votes table if it does not already exist."""
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                session_id TEXT PRIMARY KEY,
                candidate_id TEXT NOT NULL,
                candidate_name TEXT NOT NULL,
                party TEXT NOT NULL,
                cast_at TEXT NOT NULL
            )
        """)
        conn.commit()

def record_vote(session_id: str, candidate_id: str, candidate_name: str, party: str) -> bool:
    """Safely writes a single vote to SQLite. Returns False if session_id already voted."""
    try:
        with sqlite3.connect(DB_PATH, timeout=10) as conn:
            conn.execute(
                """
                INSERT INTO votes (session_id, candidate_id, candidate_name, party, cast_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (session_id, candidate_id, candidate_name, party, datetime.now(timezone.utc).isoformat())
            )
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def get_session_vote(session_id: str):
    """Checks SQLite to see if this session_id has already cast a ballot."""
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        row = conn.execute(
            "SELECT candidate_name, party FROM votes WHERE session_id = ?",
            (session_id,)
        ).fetchone()
    return f"{row[0]} ({row[1]})" if row else None

def get_vote_tally() -> dict:
    """Returns a mapping of candidate_id -> total vote count from SQLite."""
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        rows = conn.execute(
            "SELECT candidate_id, COUNT(*) FROM votes GROUP BY candidate_id"
        ).fetchall()
    return {row[0]: row[1] for row in rows}

def initialize_voter_session():
    """Ensures every unique browser session has an isolated voting token synced with SQLite."""
    init_db()
    if "voter_session_id" not in st.session_state:
        st.session_state.voter_session_id = str(uuid.uuid4())[:8]

    existing_vote = get_session_vote(st.session_state.voter_session_id)
    if existing_vote:
        st.session_state.has_voted = True
        st.session_state.voted_candidate = existing_vote
    else:
        st.session_state.setdefault("has_voted", False)
        st.session_state.setdefault("voted_candidate", None)

def render_live_tally(candidates: list):
    """Renders real-time election standings from SQLite."""
    tally = get_vote_tally()
    total_votes = sum(tally.values())

    st.markdown("---")
    st.markdown(f"### \U0001F4CA Live Election Results (Total Votes: {total_votes})")

    if total_votes == 0:
        st.caption("No ballots have been cast yet.")
        return

    sorted_candidates = sorted(
        candidates,
        key=lambda c: tally.get(c["id"], 0),
        reverse=True
    )

    for candidate in sorted_candidates:
        count = tally.get(candidate["id"], 0)
        pct = (count / total_votes) * 100
        st.markdown(f"**{candidate['name']}** `({candidate['party']})` - **{count}** votes ({pct:.1f}%)")
        st.progress(pct / 100)

def render_secure_voting_grid(candidates: list, show_live_results: bool = True):
    """Renders candidate cards with SQLite persistence, isolated keys, and live tally."""
    initialize_voter_session()

    st.markdown("### \U0001F5F3\uFE0F Official Mock Election Ballot")

    if st.session_state.has_voted:
        st.success(f"\u2705 Your vote has been permanently recorded for: **{st.session_state.voted_candidate}**")
        st.info(f"Receipt Token: `{st.session_state.voter_session_id}` - Your ballot is locked in the database.")
        if show_live_results:
            render_live_tally(candidates)
        return

    st.warning("\u26A0\uFE0F Please select your candidate carefully. Ballot submission is permanent and final.")

    for candidate in candidates:
        c_id = candidate["id"]
        c_name = candidate["name"]
        c_party = candidate["party"]

        widget_key = f"vote_{c_id}_{st.session_state.voter_session_id}"

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{c_name}** `({c_party})`")
        with col2:
            if st.button("Cast Vote", key=widget_key, type="primary"):
                saved = record_vote(
                    session_id=st.session_state.voter_session_id,
                    candidate_id=c_id,
                    candidate_name=c_name,
                    party=c_party
                )
                if saved:
                    st.session_state.has_voted = True
                    st.session_state.voted_candidate = f"{c_name} ({c_party})"
                else:
                    st.error("A ballot for this session has already been recorded.")
                st.rerun()

    if show_live_results:
        render_live_tally(candidates)
