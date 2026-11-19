import sqlite3
import os
import pandas as pd
import streamlit as st

# Strictly enforcing NDC and ADC, removing LP and NNPP
CONSTITUENCY_PARTIES = ["APC", "PDP", "NDC", "ADC", "APGA", "YPP"]

def get_db_connection():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/votes.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_id TEXT,
            polling_unit TEXT,
            ward TEXT,
            party TEXT,
            officer_type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def render_secure_voting_interface():
    init_db()
    st.markdown("### 🗳️ Secure Constituency Voting & Collation Portal")
    
    tab1, tab2 = st.tabs(["Polling Unit / Ward Ballot", "Live Election Analytical Sync"])
    
    with tab1:
        st.subheader("Cast Ballot & Collation Entry")
        with st.form("voting_form_secure"):
            voter_id = st.text_input("Voter Identification / NIN / PVC Number")
            polling_unit = st.text_input("Polling Unit Name / Code")
            ward = st.text_input("Ward Name")
            officer_type = st.selectbox("Collation Officer Level", ["Polling Unit Officer", "Ward Collation Officer"])
            
            # Party dropdown using strict CONSTITUENCY_PARTIES array
            party = st.selectbox("Select Preferred Political Party", CONSTITUENCY_PARTIES)
            
            submitted = st.form_submit_button("Submit Secure Vote")
            if submitted:
                if not voter_id or not polling_unit or not ward:
                    st.error("Please fill in all required identification fields.")
                else:
                    try:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute("SELECT id FROM votes WHERE voter_id = ?", (voter_id,))
                        if cursor.fetchone():
                            st.warning("A vote with this Identification number has already been recorded.")
                        else:
                            cursor.execute(
                                "INSERT INTO votes (voter_id, polling_unit, ward, party, officer_type) VALUES (?, ?, ?, ?, ?)",
                                (voter_id, polling_unit, ward, party, officer_type)
                            )
                            conn.commit()
                            st.success(f"Vote successfully cast and recorded under party: **{party}** ({officer_type})!")
                        conn.close()
                    except Exception as e:
                        st.error(f"Database error: {e}")

    with tab2:
        st.subheader("📊 Live Election Analytical Sync")
        try:
            conn = get_db_connection()
            df = pd.read_sql_query("SELECT * FROM votes ORDER BY timestamp DESC", conn)
            conn.close()
            
            if df.empty:
                st.info("No live votes recorded in database yet. Submit a test vote from the ballot tab to populate telemetry.")
            else:
                st.success(f"Successfully synced {len(df)} total votes from active collation feeds!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Votes Logged", len(df))
                with col2:
                    st.metric("Polling Units Reporting", df['polling_unit'].nunique() if 'polling_unit' in df.columns else 0)
                with col3:
                    st.metric("Wards Reporting", df['ward'].nunique() if 'ward' in df.columns else 0)
                
                st.markdown("### Party Performance Breakdown")
                if 'party' in df.columns and not df['party'].empty:
                    party_counts = df['party'].value_counts()
                    st.bar_chart(party_counts)
                
                st.markdown("### Secure Audit Trail & Raw Telemetry")
                st.dataframe(df, use_container_width=True)
                
        except Exception as e:
            st.warning(f"Live analytical sync pending initial database setup: {e}")
