import streamlit as st 
import requests
from dotenv import load_dotenv
import pandas as pd 
import os

# Load environment variables from .env file
load_dotenv()

# Get the BASE_URL from the .env file
BASE_URL = os.getenv("BASE_URL")
# BASE_URL = "http://localhost:8000"


st.set_page_config(layout="wide")

def count_pieces(board):
    black = sum(row.count(-1) for row in board)
    white = sum(row.count(1) for row in board)
    return black, white

def matches_to_dataframe(match_data):
    rows = []
    for match in match_data["matches"]:
        black_name = match["black_player"]["name"]
        white_name = match["white_player"]["name"]
        board = match["board"]
        status = match["status"]
        black_count, white_count = count_pieces(board)

        rows.append({
            "black_player": black_name,
            "white_player": white_name,
            "black_pieces_count": black_count,
            "white_pieces_count": white_count,
            "status": status
        })

    return pd.DataFrame(rows)

if "current_matches" not in st.session_state: 
    st.session_state.current_matches = pd.DataFrame(columns = ['Black Player', 'Black Pieces', 'White Pieces', 'White Player'])

st.title('Matches')

# Example list of players in a tournament
# players = ["Player 1", "Player 2", "Player 3", "Player 4"]

tournaments_req = requests.get(f"{BASE_URL}/tournament/list")
tournaments = tournaments_req.json().get("tournaments", [])
open_tournaments = [x for x in tournaments if x['status'] == "available"]

selected_tournament = st.selectbox("Select a tournament:", ["None"] + [t['name'] for t in open_tournaments])

if selected_tournament != "None":
    st.write(f"{selected_tournament} selected!")

    play = st.button('Start Round')

    if play: 
        pairing_req = requests.post(f"{BASE_URL}/pair/", params={"tournament_name": selected_tournament})
        
        if pairing_req.status_code == 200: 
            st.text('Lets start!!!')

            matches = matches_to_dataframe(requests.get(f"{BASE_URL}/tournament/matches/{selected_tournament}").json())
            st.session_state.current_matches = matches[matches['status'] == "ongoing"].filter(['black_player', 'black_pieces_count', 'white_pieces_count', 'white_player']).rename(
                columns={
                    'black_player': 'Black Player',
                    'black_pieces_count': 'Black Pieces',
                    'white_pieces_count': 'White Pieces',
                    'white_player': 'White Player'
                }
            )
        if pairing_req.status_code == 400: 
            st.text('Round on going')


    row_3  = st.columns([2,8,1])
    with row_3[0]:
        st.subheader("Current Matches")
    with row_3[2]: 
        refresh_matches = st.button("🔄")

    if refresh_matches:
        matches = matches_to_dataframe(requests.get(f"{BASE_URL}/tournament/matches/{selected_tournament}").json())
        st.session_state.current_matches = matches[matches['status'] == "ongoing"].filter(['black_player', 'black_pieces_count', 'white_pieces_count', 'white_player']).rename(
            columns={
                'black_player': 'Black Player',
                'black_pieces_count': 'Black Pieces',
                'white_pieces_count': 'White Pieces',
                'white_player': 'White Player'
            }
        )

    st.dataframe(st.session_state.current_matches, use_container_width = True, hide_index = True)

else:
    st.write("No tournament selected.")

