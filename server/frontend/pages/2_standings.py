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

if "tournament_data" not in st.session_state:
    st.session_state.tournament_data = pd.DataFrame(columns=["Player", "Points", "Wins", "Losses", "Draws", "Dif"])


st.title('Standings')

# Example list of players in a tournament
# players = ["Player 1", "Player 2", "Player 3", "Player 4"]

tournaments_req = requests.get(f"{BASE_URL}/tournament/list")
tournaments = tournaments_req.json().get("tournaments", [])
open_tournaments = [x for x in tournaments if x['status'] == "available"]

selected_tournament = st.selectbox("Select a tournament:", ["None"] + [t['name'] for t in open_tournaments])

if selected_tournament != "None":
    st.header(f"You selected: {selected_tournament}")

    players_req = requests.get(f"{BASE_URL}/tournament/players/{selected_tournament}")   
    players_req = pd.DataFrame(players_req.json()['players'])

    if len(players_req) > 0:

        players_req['points'] = players_req['wins'] * 3 + players_req['draws']

        st.session_state.tournament_data = players_req.filter(['name', 'points', 'wins', 'draws', 'loses', 'pieces_diff']).rename(
            columns={
                'name': 'Player',
                'points': 'Points',
                'wins': 'Wins',
                'loses': 'Losses',
                'draws': 'Draws',
                'pieces_diff': 'Dif'
            }
        )

        st.session_state.tournament_data = st.session_state.tournament_data.sort_values(by = ['Points', 'Dif'], ascending = False)

        st.dataframe(st.session_state.tournament_data, use_container_width = True, hide_index = True)

        refresh = st.button('refresh')
else:
    st.write("No tournament selected.")

