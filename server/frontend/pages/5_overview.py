import streamlit as st 
from streamlit_autorefresh import st_autorefresh
import requests
from dotenv import load_dotenv
import os 
import pandas as pd 
import time

load_dotenv(override=True) 

### Page layout 

st.set_page_config(layout="wide")

### Session variables 

BASE_URL = os.getenv("BASE_URL")
# BASE_URL = "http://localhost:8000"

st_autorefresh(interval= 5000, key = 'autorefresh')

if not "available_tournaments" in st.session_state: 
    st.session_state.available_tournaments = requests.get(f"{BASE_URL}/tournament/available").json()['available_tournaments']

if not "standings" in st.session_state: 
    st.session_state.standings = pd.DataFrame(columns=["Player", "Points", "Wins", "Losses", "Draws", "Pieces Diff"])

if not "selected_tournament" in st.session_state: 
    st.session_state.selected_tournament = None

if not "round_ongoing" in st.session_state: 
    st.session_state.round_ongoing = False 

### UI
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

st.title('Othello Tournament')

st.header('Ongoing tournaments')

st.session_state.selected_tournament = st.selectbox(
    key = '_id_selected_tournament'
    , label = 'Select a tournament:'
    , options = ['Select a tournament...'] + st.session_state.available_tournaments
)

st.header('Standings')


if st.session_state.selected_tournament: 
    if st.session_state.selected_tournament == 'Select a tournament...': 
        st.session_state.standings = pd.DataFrame(columns=["Player", "Points", "Wins", "Losses", "Draws", "Pieces Diff"])
    else: 
        _standings = requests.get(f"{BASE_URL}/tournament/players/{st.session_state.selected_tournament}")  
        _standings = pd.DataFrame(_standings.json()['players']) 

        if len(_standings) > 0: 
            _standings['points'] = _standings['wins'] * 3 + _standings['draws']
            _standings = _standings.filter(['name', 'points', 'wins', 'draws', 'loses', 'pieces_diff']).rename(
                    columns={
                        'name': 'Player',
                        'points': 'Points',
                        'wins': 'Wins',
                        'loses': 'Losses',
                        'draws': 'Draws',
                        'pieces_diff': 'Pieces Diff'
                    }
                )
            st.session_state.standings = _standings.sort_values(by = ['Points', 'Pieces Diff'], ascending= False)
        else: 
            st.session_state.standings = pd.DataFrame(columns=["Player", "Points", "Wins", "Losses", "Draws", "Pieces Diff"])
    

st.dataframe(
    st.session_state.standings
    , hide_index = True 
    , use_container_width = True 
)

refresh_standings = st.button("🔄", )    

st.header("Matches")

# if not "matches" in st.session_state: 
#     st.session_state.matches = None 
if not "ongoing_matches" in st.session_state: 
    st.session_state.ongoing_matches = [] 


if st.session_state.selected_tournament and not st.session_state.selected_tournament == 'Select a tournament...': 
    st.session_state.ongoing_matches = requests.get(f"{BASE_URL}/boards/ongoing/{st.session_state.selected_tournament}").json()['ongoing_boards']

st.subheader("Live boards")

if len(st.session_state.ongoing_matches) == 0 : 
    if st.button("Play ▶️"): 
        pairing_req = requests.post(f"{BASE_URL}/pair/", params={"tournament_name": st.session_state.selected_tournament})
        if pairing_req.status_code == 200: 
            st.session_state.round_ongoing = True 

if st.session_state.round_ongoing: 
    
    st.session_state.ongoing_matches = requests.get(f"{BASE_URL}/boards/ongoing/{st.session_state.selected_tournament}").json()['ongoing_boards']

    if len(st.session_state.ongoing_matches) > 0 :
        st.session_state.round_ongoing = True
        boards_placeholder = st.empty() 
        with boards_placeholder.container():
            cols = st.columns(4)
            for i, match in enumerate(st.session_state.ongoing_matches): 
                col = cols[i % 4]
                with col: 
                    white_player = match['white_player']['name']
                    black_player = match['black_player']['name']
                    board = match['board']
                    white_score = sum(cell for row in board for cell in row if cell == 1)
                    black_score = -1 * sum(cell for row in board for cell in row if cell == -1)
                    board_df = pd.DataFrame(board)
                    board_df = board_df.replace({0 : '', -1 : '⚫️', 1 : '⚪️'})
                    st.subheader(f"⚫️ {black_player} - {black_score}")
                    st.subheader(f"⚪️ {white_player} - {white_score}")
                    st.table(board_df)
    else: 
        st.session_state.round_ongoing = False 
    
    
st.subheader("Ended Matches")

if st.session_state.selected_tournament and not st.session_state.selected_tournament == 'Select a tournament...': 
    matches = matches_to_dataframe(requests.get(f"{BASE_URL}/tournament/matches/{st.session_state.selected_tournament}").json())

    ended_matches = matches[matches['status'] == "ended"].filter(['black_player', 'black_pieces_count', 'white_pieces_count', 'white_player']).rename(
                columns={
                    'black_player': 'Black Player',
                    'black_pieces_count': 'Black Pieces',
                    'white_pieces_count': 'White Pieces',
                    'white_player': 'White Player'  
                }
            )

    ended_matches['Winner'] = ended_matches.apply(
                lambda row: row['Black Player'] if row['Black Pieces'] > row['White Pieces'] else row['White Player'] if row['White Pieces'] > row['Black Pieces'] else 'Draw',
                axis=1
            )

    st.dataframe(ended_matches, use_container_width = True, hide_index = True)