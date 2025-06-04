import streamlit as st
import pandas as pd
import requests 
from dotenv import load_dotenv
import os
# from streamlit_autorefresh import st_autorefresh
# Set Streamlit to wide mode

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

# Load environment variables from .env file
load_dotenv()

# Get the BASE_URL from the .env file
BASE_URL = os.getenv("BASE_URL")

# Initialize session state for tournament data

if "current_matches" not in st.session_state: 
    st.session_state.current_matches = pd.DataFrame(columns = ['Black Player', 'Black Pieces', 'White Pieces', 'White Player'])
if "ended_matches" not in st.session_state: 
    st.session_state.ended_matches = pd.DataFrame(columns = ['Black Player', 'Black Pieces', 'White Pieces', 'White Player', 'Winner'])
if "tournament_data" not in st.session_state:
    st.session_state.tournament_data = pd.DataFrame(columns=["Player", "Points", "Wins", "Losses", "Draws", "Dif"])


st.title('Othello Tournament')

tournament_name = st.text_input('Tournament name:')

if tournament_name: 
    ava_url = f"{BASE_URL}/tournament/available"
    print(ava_url)
    available_tournaments_req = requests.get(ava_url)
    available_tournaments = available_tournaments_req.json()['available_tournaments']

    if tournament_name not in available_tournaments: 
        create_req = requests.post(f"{BASE_URL}/tournament/create", json={"name": tournament_name})

    st.header(tournament_name)
    
    row_1  = st.columns([1,9,1])
    with row_1[0]:
        st.subheader("Standings")
    with row_1[2]: 
        refresh_players = st.button("Refresh Players")
    
    if refresh_players:
        players_req = requests.get(f"{BASE_URL}/tournament/players/{tournament_name}")   
        players_req = pd.DataFrame(players_req.json()['players'])
        players_req['points'] = players_req['wins'] * 3 + players_req['draws']

        st.session_state.tournament_data = players_req.filter(['name', 'points', 'wins', 'drawss', 'loses', 'pieces_diff']).rename(
            columns={
                'name': 'Player',
                'points': 'Points',
                'wins': 'Wins',
                'loses': 'Losses',
                'draws': 'Draws',
                'pieces_diff': 'Dif'
            }
        )
    st.dataframe(st.session_state.tournament_data, use_container_width = True, hide_index = True)

    play = st.button('Start Round')

    if play: 
        pairing_req = requests.post(f"{BASE_URL}/pair/", params={"tournament_name": tournament_name})
        
        if pairing_req.status_code == 200: 
            st.text('Lets start!!!')
        if pairing_req.status_code == 400: 
            st.text('Round on going')

    row_3  = st.columns([2,8,1])
    with row_3[0]:
        st.subheader("Current Matches")
    with row_3[2]: 
        refresh_matches = st.button("Refresh")

    if refresh_matches:
        matches = matches_to_dataframe(requests.get(f"{BASE_URL}/tournament/matches/{tournament_name}").json())
        st.session_state.current_matches = matches[matches['status'] == "ongoing"].filter(['black_player', 'black_pieces_count', 'white_pieces_count', 'white_player']).rename(
            columns={
                'black_player': 'Black Player',
                'black_pieces_count': 'Black Pieces',
                'white_pieces_count': 'White Pieces',
                'white_player': 'White Player'
            }
        )

        st.session_state.ended_matches = matches[matches['status'] == "ended"].filter(['black_player', 'black_pieces_count', 'white_pieces_count', 'white_player']).rename(
            columns={
                'black_player': 'Black Player',
                'black_pieces_count': 'Black Pieces',
                'white_pieces_count': 'White Pieces',
                'white_player': 'White Player'  
            }
        )

        st.session_state.ended_matches['Winner'] = st.session_state.ended_matches.apply(
            lambda row: row['Black Player'] if row['Black Pieces'] > row['White Pieces'] else row['White Player'] if row['White Pieces'] > row['Black Pieces'] else 'Draw',
            axis=1
        )


    st.dataframe(st.session_state.current_matches, use_container_width = True, hide_index = True)
    st.subheader("History")
    st.dataframe(st.session_state.ended_matches, use_container_width = True, hide_index = True)

